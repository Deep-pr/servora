from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from services.models import ServiceCategory
from .models import ProviderProfile, ProviderService, VerificationDocument


class ProviderManagementTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.provider_user = User.objects.create_user(
            username='providerx',
            password='StrongPass123!',
            role=User.PROVIDER,
        )
        self.customer_user = User.objects.create_user(
            username='customerx',
            password='StrongPass123!',
            role=User.CUSTOMER,
        )
        self.provider = ProviderProfile.objects.create(
            user=self.provider_user,
            business_name='Provider X',
            base_location='Tinsukia',
            service_area='Tinsukia',
        )
        self.category = ServiceCategory.objects.create(name='Electrical', slug='electrical')

    def test_provider_can_create_own_service(self):
        self.client.login(username='providerx', password='StrongPass123!')
        response = self.client.post(reverse('providers:service_create'), {
            'category': self.category.pk,
            'title': 'Fan Repair',
            'description': 'Ceiling fan repair and fitting.',
            'starting_price': '350.00',
            'is_active': 'on',
        })

        self.assertRedirects(response, reverse('providers:my_services'))
        self.assertTrue(ProviderService.objects.filter(provider=self.provider, title='Fan Repair').exists())

    def test_customer_cannot_manage_provider_services(self):
        self.client.login(username='customerx', password='StrongPass123!')
        response = self.client.get(reverse('providers:my_services'))
        self.assertEqual(response.status_code, 403)

    def test_provider_can_upload_verification_document(self):
        self.client.login(username='providerx', password='StrongPass123!')
        upload = SimpleUploadedFile('id.pdf', b'%PDF-1.4 demo', content_type='application/pdf')
        response = self.client.post(reverse('providers:verification'), {
            'document_type': 'Identity Proof',
            'document': upload,
        })

        self.assertRedirects(response, reverse('providers:verification'))
        self.assertTrue(VerificationDocument.objects.filter(provider=self.provider, status=VerificationDocument.PENDING).exists())

# Create your tests here.
