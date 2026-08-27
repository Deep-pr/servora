from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from services.models import ServiceCategory
from .models import ProviderProfile


def provider_search(request):
    query = request.GET.get('q', '').strip()
    location = request.GET.get('location', '').strip()
    providers = ProviderProfile.objects.filter(
        verification_status=ProviderProfile.APPROVED
    ).select_related('user').prefetch_related('services__category')

    if query:
        providers = providers.filter(
            Q(services__category__name__icontains=query)
            | Q(services__title__icontains=query)
            | Q(business_name__icontains=query)
        )
    if location:
        providers = providers.filter(Q(base_location__icontains=location) | Q(service_area__icontains=location))

    sort = request.GET.get('sort', 'recommended')
    if sort == 'highest_rated':
        providers = providers.order_by('-average_rating', '-trust_score')
    elif sort == 'lowest_price':
        providers = providers.order_by('services__starting_price')
    elif sort == 'most_experienced':
        providers = providers.order_by('-experience_years')
    else:
        providers = providers.order_by('-trust_score', '-average_rating')

    return render(request, 'public/provider_search.html', {
        'providers': providers.distinct(),
        'categories': ServiceCategory.objects.filter(is_active=True),
        'query': query,
        'location': location,
        'sort': sort,
    })


def provider_profile(request, pk):
    provider = get_object_or_404(
        ProviderProfile.objects.select_related('user').prefetch_related('services__category', 'reviews'),
        pk=pk,
        verification_status=ProviderProfile.APPROVED,
    )
    return render(request, 'public/provider_profile.html', {'provider': provider})

# Create your views here.
