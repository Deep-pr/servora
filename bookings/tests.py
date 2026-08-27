from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from providers.models import ProviderProfile, ProviderService
from services.models import ServiceCategory
from .models import Booking, Quote


class BookingWorkflowTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.customer = User.objects.create_user(username='customer', password='StrongPass123!')
        self.provider_user = User.objects.create_user(username='provider', password='StrongPass123!', role=User.PROVIDER)
        self.provider = ProviderProfile.objects.create(
            user=self.provider_user,
            business_name='Test Provider',
            base_location='Tinsukia',
            service_area='Tinsukia',
            verification_status=ProviderProfile.APPROVED,
        )
        self.category = ServiceCategory.objects.create(name='AC Repair', slug='ac-repair')
        self.provider_service = ProviderService.objects.create(
            provider=self.provider,
            category=self.category,
            title='AC Service',
            description='AC repair and cleaning.',
            starting_price=Decimal('500.00'),
        )

    def test_customer_can_create_booking(self):
        self.client.login(username='customer', password='StrongPass123!')
        response = self.client.post(reverse('bookings:create', args=[self.provider.pk]), {
            'provider_service': self.provider_service.pk,
            'scheduled_for': (timezone.now() + timezone.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M'),
            'address': 'AT Road, Tinsukia',
            'problem_description': 'AC is not cooling.',
            'contact_preference': 'phone',
        })

        booking = Booking.objects.get(customer=self.customer)
        self.assertRedirects(response, reverse('bookings:detail', args=[booking.pk]))
        self.assertEqual(booking.status, Booking.PENDING)
        self.assertEqual(booking.estimated_amount, self.provider_service.starting_price)

    def test_provider_can_accept_booking(self):
        booking = self._create_booking()
        self.client.login(username='provider', password='StrongPass123!')
        response = self.client.post(reverse('bookings:provider_update_status', args=[booking.pk, Booking.ACCEPTED]))

        booking.refresh_from_db()
        self.assertRedirects(response, reverse('bookings:detail', args=[booking.pk]))
        self.assertEqual(booking.status, Booking.ACCEPTED)

    def test_provider_can_send_quote_and_customer_can_accept(self):
        booking = self._create_booking()
        self.client.login(username='provider', password='StrongPass123!')
        response = self.client.post(reverse('bookings:quote_create', args=[booking.pk]), {
            'estimated_price': '750.00',
            'service_description': 'Full AC inspection and gas refill.',
            'expected_completion_time': '2 hours',
            'notes': 'Includes visit charge.',
            'expires_at': (timezone.now() + timezone.timedelta(days=2)).strftime('%Y-%m-%dT%H:%M'),
        })

        quote = Quote.objects.get(booking=booking)
        self.assertRedirects(response, reverse('bookings:detail', args=[booking.pk]))
        self.assertEqual(quote.status, Quote.PENDING)

        self.client.logout()
        self.client.login(username='customer', password='StrongPass123!')
        response = self.client.post(reverse('bookings:quote_decision', args=[quote.pk, Quote.ACCEPTED]))

        booking.refresh_from_db()
        quote.refresh_from_db()
        self.assertRedirects(response, reverse('bookings:detail', args=[booking.pk]))
        self.assertEqual(quote.status, Quote.ACCEPTED)
        self.assertEqual(booking.status, Booking.CONFIRMED)

    def _create_booking(self):
        return Booking.objects.create(
            customer=self.customer,
            provider=self.provider,
            provider_service=self.provider_service,
            scheduled_for=timezone.now() + timezone.timedelta(days=1),
            address='AT Road, Tinsukia',
            problem_description='AC is not cooling.',
            estimated_amount=self.provider_service.starting_price,
        )

# Create your tests here.
