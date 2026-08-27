from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import User
from providers.models import ProviderProfile
from .forms import BookingForm, QuoteForm
from .models import Booking, Quote


@login_required
def my_bookings(request):
    if request.user.role == User.PROVIDER:
        provider = get_object_or_404(ProviderProfile, user=request.user)
        bookings = Booking.objects.filter(provider=provider).select_related('customer', 'provider_service')
        return render(request, 'bookings/provider_bookings.html', {'bookings': bookings})

    bookings = Booking.objects.filter(customer=request.user).select_related('provider', 'provider_service')
    return render(request, 'bookings/customer_bookings.html', {'bookings': bookings})


@login_required
def booking_create(request, provider_id):
    if request.user.role != User.CUSTOMER:
        raise PermissionDenied
    provider = get_object_or_404(ProviderProfile, pk=provider_id, verification_status=ProviderProfile.APPROVED)
    form = BookingForm(request.POST or None, provider=provider)
    if request.method == 'POST' and form.is_valid():
        booking = form.save(commit=False)
        booking.customer = request.user
        booking.provider = provider
        booking.status = Booking.PENDING
        booking.estimated_amount = booking.provider_service.starting_price
        booking.save()
        messages.success(request, 'Booking request sent to provider.')
        return redirect('bookings:detail', pk=booking.pk)
    return render(request, 'bookings/booking_form.html', {'form': form, 'provider': provider})


@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(
        Booking.objects.select_related('customer', 'provider', 'provider_service').prefetch_related('quotes'),
        pk=pk,
    )
    _assert_booking_access(request.user, booking)
    quote_form = QuoteForm() if request.user.role == User.PROVIDER else None
    booking_actions = [
        (Booking.ACCEPTED, 'Accept'),
        (Booking.REJECTED, 'Reject'),
        (Booking.CONFIRMED, 'Confirm'),
        (Booking.ON_THE_WAY, 'On The Way'),
        (Booking.WORK_STARTED, 'Work Started'),
        (Booking.COMPLETED, 'Completed'),
        (Booking.RESCHEDULED, 'Reschedule'),
        (Booking.DISPUTED, 'Dispute'),
    ]
    can_cancel = booking.status not in {Booking.COMPLETED, Booking.REVIEWED, Booking.CANCELLED}
    return render(request, 'bookings/booking_detail.html', {
        'booking': booking,
        'quote_form': quote_form,
        'booking_actions': booking_actions,
        'can_cancel': can_cancel,
    })


@login_required
def booking_cancel(request, pk):
    booking = get_object_or_404(Booking, pk=pk, customer=request.user)
    if request.method == 'POST':
        booking.status = Booking.CANCELLED
        booking.save(update_fields=['status', 'updated_at'])
        messages.success(request, 'Booking cancelled.')
    return redirect('bookings:detail', pk=booking.pk)


@login_required
def provider_update_status(request, pk, status):
    provider = get_object_or_404(ProviderProfile, user=request.user)
    booking = get_object_or_404(Booking, pk=pk, provider=provider)
    allowed = {
        Booking.ACCEPTED,
        Booking.REJECTED,
        Booking.CONFIRMED,
        Booking.ON_THE_WAY,
        Booking.WORK_STARTED,
        Booking.COMPLETED,
        Booking.RESCHEDULED,
        Booking.DISPUTED,
    }
    if status not in allowed:
        raise PermissionDenied
    if request.method == 'POST':
        booking.status = status
        booking.save(update_fields=['status', 'updated_at'])
        messages.success(request, f'Booking marked as {booking.get_status_display()}.')
    return redirect('bookings:detail', pk=booking.pk)


@login_required
def quote_create(request, booking_id):
    provider = get_object_or_404(ProviderProfile, user=request.user)
    booking = get_object_or_404(Booking, pk=booking_id, provider=provider)
    form = QuoteForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        quote = form.save(commit=False)
        quote.booking = booking
        quote.provider = provider
        quote.save()
        booking.estimated_amount = quote.estimated_price
        booking.save(update_fields=['estimated_amount', 'updated_at'])
        messages.success(request, 'Quote sent to customer.')
    return redirect('bookings:detail', pk=booking.pk)


@login_required
def quote_decision(request, pk, status):
    quote = get_object_or_404(Quote.objects.select_related('booking'), pk=pk, booking__customer=request.user)
    if status not in {Quote.ACCEPTED, Quote.REJECTED}:
        raise PermissionDenied
    if request.method == 'POST':
        quote.status = status
        quote.save(update_fields=['status'])
        if status == Quote.ACCEPTED:
            quote.booking.status = Booking.CONFIRMED
            quote.booking.estimated_amount = quote.estimated_price
            quote.booking.save(update_fields=['status', 'estimated_amount', 'updated_at'])
        messages.success(request, f'Quote {quote.get_status_display().lower()}.')
    return redirect('bookings:detail', pk=quote.booking.pk)


def _assert_booking_access(user, booking):
    if user.is_staff or user.role == User.ADMIN:
        return
    if booking.customer_id == user.id:
        return
    if user.role == User.PROVIDER and booking.provider.user_id == user.id:
        return
    raise PermissionDenied

# Create your views here.
