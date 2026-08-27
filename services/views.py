from django.shortcuts import get_object_or_404, render

from providers.models import ProviderProfile
from .models import ServiceCategory


def service_list(request):
    categories = ServiceCategory.objects.filter(is_active=True)
    return render(request, 'public/services.html', {'categories': categories})


def service_detail(request, slug):
    category = get_object_or_404(ServiceCategory, slug=slug, is_active=True)
    providers = ProviderProfile.objects.filter(
        services__category=category,
        services__is_active=True,
        verification_status=ProviderProfile.APPROVED,
    ).select_related('user').distinct()
    return render(request, 'public/service_detail.html', {'category': category, 'providers': providers})

# Create your views here.
