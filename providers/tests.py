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


class ProviderSearchTests(TestCase):
    def setUp(self):
        User = get_user_model()
        category = ServiceCategory.objects.create(name='Plumbing', slug='plumbing')
        for index, data in enumerate([
            ('Near Pro', '27.488600', '95.355800', 5, '4.80', 250, True),
            ('Far Pro', '27.560000', '95.410000', 12, '4.20', 900, False),
        ]):
            user = User.objects.create_user(
                username=f'searchprovider{index}',
                password='StrongPass123!',
                role=User.PROVIDER,
            )
            provider = ProviderProfile.objects.create(
                user=user,
                business_name=data[0],
                base_location='Tinsukia',
                service_area='Tinsukia',
                latitude=data[1],
                longitude=data[2],
                experience_years=data[3],
                average_rating=data[4],
                trust_score=80 + index,
                emergency_available=data[6],
                verification_status=ProviderProfile.APPROVED,
            )
            ProviderService.objects.create(
                provider=provider,
                category=category,
                title='Plumbing Service',
                description='Reliable plumbing support.',
                starting_price=data[5],
            )

    def test_search_filters_by_rating_price_and_emergency(self):
        response = self.client.get(reverse('providers:search'), {
            'q': 'Plumbing',
            'min_rating': '4.5',
            'max_price': '300',
            'emergency': 'on',
        })

        self.assertContains(response, 'Near Pro')
        self.assertNotContains(response, 'Far Pro')

    def test_search_can_sort_by_nearest_with_coordinates(self):
        response = self.client.get(reverse('providers:search'), {
            'q': 'Plumbing',
            'lat': '27.488600',
            'lng': '95.355800',
            'sort': 'nearest',
        })

        providers = list(response.context['providers'])
        self.assertEqual(providers[0].business_name, 'Near Pro')
        self.assertLess(providers[0].distance_km, providers[1].distance_km)

# Create your tests here.
