from django import forms
from django.contrib.auth.forms import UserCreationForm

from providers.models import ProviderProfile
from .models import CustomerProfile, User


class CustomerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=False)
    city = forms.CharField(max_length=100, required=True)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'city', 'address')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.CUSTOMER
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data.get('phone', '')
        if commit:
            user.save()
            CustomerProfile.objects.create(
                user=user,
                city=self.cleaned_data['city'],
                address=self.cleaned_data.get('address', ''),
            )
        return user


class ProviderRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True)
    business_name = forms.CharField(max_length=160)
    base_location = forms.CharField(max_length=160)
    service_area = forms.CharField(max_length=160)
    experience_years = forms.IntegerField(min_value=0, max_value=60)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))
    emergency_available = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'phone',
            'business_name', 'base_location', 'service_area',
            'experience_years', 'bio', 'emergency_available',
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.PROVIDER
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        if commit:
            user.save()
            ProviderProfile.objects.create(
                user=user,
                business_name=self.cleaned_data['business_name'],
                base_location=self.cleaned_data['base_location'],
                service_area=self.cleaned_data['service_area'],
                experience_years=self.cleaned_data['experience_years'],
                bio=self.cleaned_data['bio'],
                emergency_available=self.cleaned_data['emergency_available'],
            )
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone')


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ('profile_photo', 'city', 'address', 'latitude', 'longitude')


class ProviderProfileForm(forms.ModelForm):
    class Meta:
        model = ProviderProfile
        fields = (
            'business_name', 'bio', 'experience_years', 'service_area',
            'base_location', 'latitude', 'longitude', 'profile_photo',
            'emergency_available',
        )
