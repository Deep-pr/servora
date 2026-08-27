from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from providers.models import ProviderProfile
from .forms import (
    CustomerProfileForm,
    CustomerRegistrationForm,
    ProviderProfileForm,
    ProviderRegistrationForm,
    UserProfileForm,
)
from .models import CustomerProfile, User


def register(request):
    return render(request, 'accounts/register_choice.html')


def customer_register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Customer account created successfully.')
            return redirect('dashboard:home')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form, 'title': 'Customer Registration'})


def provider_register(request):
    if request.method == 'POST':
        form = ProviderRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Provider account created. Complete verification to become approved.')
            return redirect('dashboard:home')
    else:
        form = ProviderRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form, 'title': 'Provider Registration'})


@login_required
def profile(request):
    user_form = UserProfileForm(request.POST or None, instance=request.user)

    if request.user.role == User.PROVIDER:
        provider_profile, _ = ProviderProfile.objects.get_or_create(
            user=request.user,
            defaults={
                'business_name': request.user.get_full_name() or request.user.username,
                'base_location': '',
                'service_area': '',
            },
        )
        role_form = ProviderProfileForm(request.POST or None, request.FILES or None, instance=provider_profile)
        template = 'accounts/provider_profile_form.html'
    else:
        customer_profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
        role_form = CustomerProfileForm(request.POST or None, instance=customer_profile)
        template = 'accounts/customer_profile_form.html'

    if request.method == 'POST' and user_form.is_valid() and role_form.is_valid():
        user_form.save()
        role_form.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('accounts:profile')

    return render(request, template, {'user_form': user_form, 'role_form': role_form})

# Create your views here.
