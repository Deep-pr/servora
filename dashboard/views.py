from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from bookings.models import Booking
from providers.models import ProviderProfile
from services.models import ServiceCategory
from accounts.models import User


def home(request):
    categories = ServiceCategory.objects.filter(is_active=True)[:8]
    providers = ProviderProfile.objects.filter(
        verification_status=ProviderProfile.APPROVED
    ).select_related('user')[:6]
    return render(request, 'public/home.html', {'categories': categories, 'providers': providers})


def about(request):
    return render(request, 'public/about.html')


def contact(request):
    return render(request, 'public/contact.html')


def faq(request):
    return render(request, 'public/faq.html')


@login_required
def dashboard_home(request):
    if request.user.role == User.PROVIDER:
        provider = getattr(request.user, 'provider_profile', None)
        context = {
            'provider': provider,
            'today_count': 0,
            'pending_count': Booking.objects.filter(provider=provider, status=Booking.PENDING).count() if provider else 0,
            'completed_count': Booking.objects.filter(provider=provider, status=Booking.COMPLETED).count() if provider else 0,
            'cancelled_count': Booking.objects.filter(provider=provider, status=Booking.CANCELLED).count() if provider else 0,
        }
        return render(request, 'dashboard/provider_home.html', context)

    if request.user.is_staff or request.user.role == User.ADMIN:
        context = {
            'bookings_count': Booking.objects.count(),
            'providers_count': ProviderProfile.objects.count(),
            'verified_count': ProviderProfile.objects.filter(verification_status=ProviderProfile.APPROVED).count(),
            'users_count': User.objects.count(),
        }
        return render(request, 'dashboard/admin_home.html', context)

    context = {
        'upcoming_count': Booking.objects.filter(customer=request.user, status__in=[Booking.PENDING, Booking.ACCEPTED, Booking.CONFIRMED]).count(),
        'completed_count': Booking.objects.filter(customer=request.user, status=Booking.COMPLETED).count(),
        'cancelled_count': Booking.objects.filter(customer=request.user, status=Booking.CANCELLED).count(),
        'favorites_count': request.user.favorites.count(),
    }
    return render(request, 'dashboard/customer_home.html', context)

# Create your views here.
