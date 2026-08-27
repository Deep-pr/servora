import math

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Min, Q
from django.shortcuts import get_object_or_404, redirect, render

from services.models import ServiceCategory
from .forms import ProviderServiceForm, VerificationDocumentForm
from .models import ProviderProfile, ProviderService


def provider_search(request):
    query = request.GET.get('q', '').strip()
    location = request.GET.get('location', '').strip()
    category_id = request.GET.get('category', '').strip()
    min_rating = request.GET.get('min_rating', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    min_experience = request.GET.get('min_experience', '').strip()
    radius = request.GET.get('radius', '').strip()
    user_lat = request.GET.get('lat', '').strip()
    user_lng = request.GET.get('lng', '').strip()
    emergency = request.GET.get('emergency') == 'on'
    providers = ProviderProfile.objects.filter(
        verification_status=ProviderProfile.APPROVED
    ).select_related('user').prefetch_related('services__category').annotate(lowest_price=Min('services__starting_price'))

    if query:
        providers = providers.filter(
            Q(services__category__name__icontains=query)
            | Q(services__title__icontains=query)
            | Q(business_name__icontains=query)
        )
    if location:
        providers = providers.filter(Q(base_location__icontains=location) | Q(service_area__icontains=location))
    if category_id:
        providers = providers.filter(services__category_id=category_id)
    if min_rating:
        providers = providers.filter(average_rating__gte=min_rating)
    if max_price:
        providers = providers.filter(services__starting_price__lte=max_price)
    if min_experience:
        providers = providers.filter(experience_years__gte=min_experience)
    if emergency:
        providers = providers.filter(emergency_available=True)

    sort = request.GET.get('sort', 'recommended')
    if sort == 'highest_rated':
        providers = providers.order_by('-average_rating', '-trust_score')
    elif sort == 'lowest_price':
        providers = providers.order_by('lowest_price')
    elif sort == 'most_experienced':
        providers = providers.order_by('-experience_years')
    else:
        providers = providers.order_by('-trust_score', '-average_rating')

    provider_list = list(providers.distinct())
    user_coordinates = _parse_coordinates(user_lat, user_lng)
    radius_km = _parse_float(radius)
    if user_coordinates:
        for provider in provider_list:
            provider.distance_km = _distance_km(
                user_coordinates[0],
                user_coordinates[1],
                provider.latitude,
                provider.longitude,
            )
        if radius_km:
            provider_list = [
                provider for provider in provider_list
                if provider.distance_km is not None and provider.distance_km <= radius_km
            ]
        if sort == 'nearest':
            provider_list.sort(key=lambda provider: provider.distance_km if provider.distance_km is not None else 9999)

    paginator = Paginator(provider_list, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    query_params = request.GET.copy()
    query_params.pop('page', None)
    map_markers = [
        {
            'name': provider.business_name,
            'lat': float(provider.latitude),
            'lng': float(provider.longitude),
            'rating': float(provider.average_rating),
            'trust_score': provider.trust_score,
            'url': request.build_absolute_uri(provider.get_public_url()),
        }
        for provider in page_obj
        if provider.latitude is not None and provider.longitude is not None
    ]

    return render(request, 'public/provider_search.html', {
        'providers': page_obj,
        'page_obj': page_obj,
        'categories': ServiceCategory.objects.filter(is_active=True),
        'map_markers': map_markers,
        'query_params': query_params.urlencode(),
        'query': query,
        'location': location,
        'sort': sort,
        'filters': {
            'category': category_id,
            'min_rating': min_rating,
            'max_price': max_price,
            'min_experience': min_experience,
            'radius': radius,
            'lat': user_lat,
            'lng': user_lng,
            'emergency': emergency,
        },
    })


def provider_profile(request, pk):
    provider = get_object_or_404(
        ProviderProfile.objects.select_related('user').prefetch_related('services__category', 'reviews'),
        pk=pk,
        verification_status=ProviderProfile.APPROVED,
    )
    return render(request, 'public/provider_profile.html', {'provider': provider})


def _parse_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _parse_coordinates(latitude, longitude):
    parsed_lat = _parse_float(latitude)
    parsed_lng = _parse_float(longitude)
    if parsed_lat is None or parsed_lng is None:
        return None
    return parsed_lat, parsed_lng


def _distance_km(origin_lat, origin_lng, destination_lat, destination_lng):
    if destination_lat is None or destination_lng is None:
        return None
    lat1 = math.radians(float(origin_lat))
    lng1 = math.radians(float(origin_lng))
    lat2 = math.radians(float(destination_lat))
    lng2 = math.radians(float(destination_lng))
    delta_lat = lat2 - lat1
    delta_lng = lng2 - lng1
    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lng / 2) ** 2
    return round(6371 * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)), 1)


def _current_provider(user):
    if not user.is_authenticated or not user.is_provider():
        raise PermissionDenied
    return get_object_or_404(ProviderProfile, user=user)


@login_required
def my_services(request):
    provider = _current_provider(request.user)
    services = provider.services.select_related('category')
    return render(request, 'providers/my_services.html', {'provider': provider, 'services': services})


@login_required
def service_create(request):
    provider = _current_provider(request.user)
    form = ProviderServiceForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        provider_service = form.save(commit=False)
        provider_service.provider = provider
        provider_service.save()
        messages.success(request, 'Service added successfully.')
        return redirect('providers:my_services')
    return render(request, 'providers/service_form.html', {'form': form, 'title': 'Add Service'})


@login_required
def service_update(request, pk):
    provider = _current_provider(request.user)
    provider_service = get_object_or_404(ProviderService, pk=pk, provider=provider)
    form = ProviderServiceForm(request.POST or None, instance=provider_service)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Service updated successfully.')
        return redirect('providers:my_services')
    return render(request, 'providers/service_form.html', {'form': form, 'title': 'Edit Service'})


@login_required
def service_delete(request, pk):
    provider = _current_provider(request.user)
    provider_service = get_object_or_404(ProviderService, pk=pk, provider=provider)
    if request.method == 'POST':
        provider_service.delete()
        messages.success(request, 'Service removed successfully.')
        return redirect('providers:my_services')
    return render(request, 'providers/service_confirm_delete.html', {'provider_service': provider_service})


@login_required
def verification(request):
    provider = _current_provider(request.user)
    form = VerificationDocumentForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        document = form.save(commit=False)
        document.provider = provider
        document.save()
        provider.verification_status = ProviderProfile.PENDING
        provider.save(update_fields=['verification_status'])
        messages.success(request, 'Document uploaded for admin review.')
        return redirect('providers:verification')
    return render(request, 'providers/verification.html', {
        'provider': provider,
        'form': form,
        'documents': provider.verification_documents.all(),
    })
