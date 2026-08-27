from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import User
from bookings.models import Booking
from notifications.models import Notification
from providers.models import ProviderProfile
from .forms import ReviewForm
from .models import Favorite, Review


@login_required
def my_reviews(request):
    if request.user.role == User.PROVIDER:
        provider = get_object_or_404(ProviderProfile, user=request.user)
        reviews = Review.objects.filter(provider=provider).select_related('customer', 'booking')
    else:
        reviews = Review.objects.filter(customer=request.user).select_related('provider', 'booking')
    return render(request, 'reviews/my_reviews.html', {'reviews': reviews})


@login_required
def review_create(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, customer=request.user, status=Booking.COMPLETED)
    if hasattr(booking, 'review'):
        messages.info(request, 'You already reviewed this booking.')
        return redirect('bookings:detail', pk=booking.pk)
    form = ReviewForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        review = form.save(commit=False)
        review.booking = booking
        review.customer = request.user
        review.provider = booking.provider
        review.save()
        booking.status = Booking.REVIEWED
        booking.save(update_fields=['status', 'updated_at'])
        average = Review.objects.filter(provider=booking.provider).aggregate(value=Avg('overall_rating'))['value'] or 0
        booking.provider.average_rating = round(average, 2)
        booking.provider.save(update_fields=['average_rating'])
        Notification.objects.create(
            user=booking.provider.user,
            title='New review received',
            message=f'{request.user.username} reviewed {booking.provider_service.title}.',
            link=f'/bookings/{booking.pk}/',
        )
        messages.success(request, 'Review submitted successfully.')
        return redirect('bookings:detail', pk=booking.pk)
    return render(request, 'reviews/review_form.html', {'form': form, 'booking': booking})


@login_required
def favorite_toggle(request, provider_id):
    if request.user.role != User.CUSTOMER:
        raise PermissionDenied
    provider = get_object_or_404(ProviderProfile, pk=provider_id, verification_status=ProviderProfile.APPROVED)
    favorite, created = Favorite.objects.get_or_create(customer=request.user, provider=provider)
    if not created:
        favorite.delete()
        messages.success(request, 'Provider removed from favorites.')
    else:
        messages.success(request, 'Provider saved to favorites.')
    return redirect('providers:profile', pk=provider.pk)


@login_required
def my_favorites(request):
    favorites = Favorite.objects.filter(customer=request.user).select_related('provider', 'provider__user')
    return render(request, 'reviews/my_favorites.html', {'favorites': favorites})

# Create your views here.
