from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from providers.models import ProviderProfile
from .models import CustomerProfile, User

TINY_GIF = (
    b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00\x00'
    b'\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
)


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


class ProfilePhotoTests(TestCase):
    def test_customer_can_upload_profile_photo(self):
        user = User.objects.create_user(username='photo_customer', password='StrongPass123!')
        CustomerProfile.objects.create(user=user, city='Tinsukia')
        self.client.login(username='photo_customer', password='StrongPass123!')
        image = SimpleUploadedFile('avatar.gif', TINY_GIF, content_type='image/gif')

        response = self.client.post(reverse('accounts:profile'), {
            'first_name': 'Photo',
            'last_name': 'Customer',
            'email': 'photo@example.com',
            'phone': '9999999999',
            'profile_photo': image,
            'city': 'Tinsukia',
            'address': 'AT Road',
            'latitude': '',
            'longitude': '',
        })

        user.customer_profile.refresh_from_db()
        self.assertRedirects(response, reverse('accounts:profile'))
        self.assertTrue(user.customer_profile.profile_photo.name.startswith('customers/photos/'))

    def test_provider_can_upload_profile_photo(self):
        user = User.objects.create_user(username='photo_provider', password='StrongPass123!', role=User.PROVIDER)
        ProviderProfile.objects.create(
            user=user,
            business_name='Photo Provider',
            base_location='Tinsukia',
            service_area='Tinsukia',
        )
        self.client.login(username='photo_provider', password='StrongPass123!')
        image = SimpleUploadedFile('provider.gif', TINY_GIF, content_type='image/gif')

        response = self.client.post(reverse('accounts:profile'), {
            'first_name': 'Photo',
            'last_name': 'Provider',
            'email': 'provider@example.com',
            'phone': '8888888888',
            'business_name': 'Photo Provider',
            'bio': 'Provider bio',
            'experience_years': 4,
            'service_area': 'Tinsukia',
            'base_location': 'Tinsukia',
            'latitude': '',
            'longitude': '',
            'profile_photo': image,
        })

        user.provider_profile.refresh_from_db()
        self.assertRedirects(response, reverse('accounts:profile'))
        self.assertTrue(user.provider_profile.profile_photo.name.startswith('providers/photos/'))

# Create your tests here.
