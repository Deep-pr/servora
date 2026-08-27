from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render

from providers.models import ProviderProfile
from .forms import ServiceCategoryForm
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


@staff_member_required
def category_manage(request):
    categories = ServiceCategory.objects.all()
    return render(request, 'services/category_manage.html', {'categories': categories})


@staff_member_required
def category_create(request):
    form = ServiceCategoryForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Service category created.')
        return redirect('services:category_manage')
    return render(request, 'services/category_form.html', {'form': form, 'title': 'Add Category'})


@staff_member_required
def category_update(request, pk):
    category = get_object_or_404(ServiceCategory, pk=pk)
    form = ServiceCategoryForm(request.POST or None, instance=category)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Service category updated.')
        return redirect('services:category_manage')
    return render(request, 'services/category_form.html', {'form': form, 'title': 'Edit Category'})


@staff_member_required
def category_delete(request, pk):
    category = get_object_or_404(ServiceCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Service category removed.')
        return redirect('services:category_manage')
    return render(request, 'services/category_confirm_delete.html', {'category': category})
