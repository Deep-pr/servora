from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from bookings.models import Booking
from notifications.models import Notification
from providers.models import ProviderProfile, ProviderService
from services.models import ServiceCategory
from .models import Complaint


class ComplaintTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.admin = User.objects.create_user(username='adminuser', password='StrongPass123!', is_staff=True)
        self.customer = User.objects.create_user(username='complaintcustomer', password='StrongPass123!')
        provider_user = User.objects.create_user(username='complaintprovider', password='StrongPass123!', role=User.PROVIDER)
        provider = ProviderProfile.objects.create(
            user=provider_user,
            business_name='Complaint Provider',
            base_location='Tinsukia',
            service_area='Tinsukia',
            verification_status=ProviderProfile.APPROVED,
        )
        category = ServiceCategory.objects.create(name='Painting', slug='painting')
        service = ProviderService.objects.create(provider=provider, category=category, title='Wall Painting', starting_price='800.00')
        self.booking = Booking.objects.create(
            customer=self.customer,
            provider=provider,
            provider_service=service,
            scheduled_for=timezone.now(),
            address='AT Road',
            problem_description='Painting request.',
        )

    def test_customer_can_submit_complaint(self):
        self.client.login(username='complaintcustomer', password='StrongPass123!')
        response = self.client.post(reverse('complaints:create'), {
            'booking': self.booking.pk,
            'category': 'Poor service',
            'description': 'Provider did not arrive on time.',
        })

        self.assertRedirects(response, reverse('complaints:my_complaints'))
        self.assertTrue(Complaint.objects.filter(customer=self.customer, category='Poor service').exists())
        self.assertTrue(Notification.objects.filter(user=self.admin, title='New complaint submitted').exists())

# Create your tests here.
