from django.test import TestCase
from django.urls import reverse

from providers.models import ProviderProfile
from .models import CustomerProfile, User


class RegistrationFlowTests(TestCase):
    def test_customer_registration_creates_customer_profile(self):
        response = self.client.post(reverse('accounts:customer_register'), {
            'username': 'newcustomer',
            'first_name': 'New',
            'last_name': 'Customer',
            'email': 'newcustomer@example.com',
            'phone': '9876543210',
            'city': 'Tinsukia',
            'address': 'Station Road',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })

        self.assertRedirects(response, reverse('dashboard:home'))
        user = User.objects.get(username='newcustomer')
        self.assertEqual(user.role, User.CUSTOMER)
        self.assertTrue(CustomerProfile.objects.filter(user=user, city='Tinsukia').exists())

    def test_provider_registration_creates_pending_provider_profile(self):
        response = self.client.post(reverse('accounts:provider_register'), {
            'username': 'newprovider',
            'first_name': 'New',
            'last_name': 'Provider',
            'email': 'newprovider@example.com',
            'phone': '9876543210',
            'business_name': 'New Provider Services',
            'base_location': 'Tinsukia',
            'service_area': 'Tinsukia and nearby towns',
            'experience_years': 5,
            'bio': 'Reliable local services.',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })

        self.assertRedirects(response, reverse('dashboard:home'))
        user = User.objects.get(username='newprovider')
        provider = ProviderProfile.objects.get(user=user)
        self.assertEqual(user.role, User.PROVIDER)
        self.assertEqual(provider.verification_status, ProviderProfile.PENDING)


class DashboardAccessTests(TestCase):
    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 302)

# Create your tests here.
