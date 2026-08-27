from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from bookings.models import Booking
from notifications.models import Notification
from providers.models import ProviderProfile, ProviderService
from services.models import ServiceCategory
from .models import Favorite, Review


class ReviewAndFavoriteTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.customer = User.objects.create_user(username='reviewcustomer', password='StrongPass123!')
        provider_user = User.objects.create_user(username='reviewprovider', password='StrongPass123!', role=User.PROVIDER)
        self.provider = ProviderProfile.objects.create(
            user=provider_user,
            business_name='Review Provider',
            base_location='Tinsukia',
            service_area='Tinsukia',
            verification_status=ProviderProfile.APPROVED,
        )
        category = ServiceCategory.objects.create(name='Cleaning', slug='cleaning')
        self.service = ProviderService.objects.create(
            provider=self.provider,
            category=category,
            title='Deep Cleaning',
            starting_price='400.00',
        )
        self.booking = Booking.objects.create(
            customer=self.customer,
            provider=self.provider,
            provider_service=self.service,
            scheduled_for=timezone.now(),
            address='AT Road',
            problem_description='Need cleaning.',
            status=Booking.COMPLETED,
        )

    def test_customer_can_favorite_provider(self):
        self.client.login(username='reviewcustomer', password='StrongPass123!')
        response = self.client.post(reverse('reviews:favorite_toggle', args=[self.provider.pk]))

        self.assertRedirects(response, reverse('providers:profile', args=[self.provider.pk]))
        self.assertTrue(Favorite.objects.filter(customer=self.customer, provider=self.provider).exists())

    def test_customer_can_review_completed_booking(self):
        self.client.login(username='reviewcustomer', password='StrongPass123!')
        response = self.client.post(reverse('reviews:create', args=[self.booking.pk]), {
            'overall_rating': 5,
            'service_quality': 5,
            'professionalism': 5,
            'punctuality': 4,
            'pricing': 4,
            'comment': 'Excellent work.',
        })

        self.booking.refresh_from_db()
        self.assertRedirects(response, reverse('bookings:detail', args=[self.booking.pk]))
        self.assertEqual(self.booking.status, Booking.REVIEWED)
        self.assertTrue(Review.objects.filter(booking=self.booking).exists())
        self.assertTrue(Notification.objects.filter(user=self.provider.user, title='New review received').exists())

# Create your tests here.
