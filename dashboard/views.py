from django.shortcuts import render

from bookings.models import Booking
from providers.models import ProviderProfile
from services.models import ServiceCategory


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


def dashboard_home(request):
    context = {
        'bookings_count': Booking.objects.count(),
        'providers_count': ProviderProfile.objects.count(),
        'verified_count': ProviderProfile.objects.filter(verification_status=ProviderProfile.APPROVED).count(),
    }
    return render(request, 'dashboard/home.html', context)

# Create your views here.
