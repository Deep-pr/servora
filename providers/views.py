from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from services.models import ServiceCategory
from .forms import ProviderServiceForm, VerificationDocumentForm
from .models import ProviderProfile, ProviderService


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
