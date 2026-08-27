from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from bookings.models import Booking
from providers.models import ProviderProfile, ProviderService
from services.models import ServiceCategory
from .models import AuditLog
from .services import analytics_chart_data, platform_metrics


class AnalyticsDashboardTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.staff = User.objects.create_user(username='analyticsstaff', password='StrongPass123!', is_staff=True)
        self.customer = User.objects.create_user(username='analyticscustomer', password='StrongPass123!')
        provider_user = User.objects.create_user(username='analyticsprovider', password='StrongPass123!', role=User.PROVIDER)
        self.provider = ProviderProfile.objects.create(
            user=provider_user,
            business_name='Analytics Provider',
            base_location='Tinsukia',
            service_area='Tinsukia',
            verification_status=ProviderProfile.APPROVED,
        )
        category = ServiceCategory.objects.create(name='Appliance Repair', slug='appliance-repair')
        service = ProviderService.objects.create(provider=self.provider, category=category, title='Fridge Repair', starting_price='900.00')
        Booking.objects.create(
            customer=self.customer,
            provider=self.provider,
            provider_service=service,
            scheduled_for=timezone.now(),
            address='AT Road',
            problem_description='Fridge cooling issue.',
            status=Booking.COMPLETED,
            estimated_amount='900.00',
        )

    def test_staff_can_view_analytics_dashboard(self):
        self.client.login(username='analyticsstaff', password='StrongPass123!')
        response = self.client.get(reverse('analytics:dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Analytics Dashboard')

    def test_non_staff_cannot_view_analytics_dashboard(self):
        self.client.login(username='analyticscustomer', password='StrongPass123!')
        response = self.client.get(reverse('analytics:dashboard'))

        self.assertEqual(response.status_code, 302)

    def test_metrics_and_chart_data_are_generated(self):
        metrics = platform_metrics()
        charts = analytics_chart_data()

        self.assertEqual(metrics['total_bookings'], 1)
        self.assertIn('booking_trends', charts)
        self.assertGreaterEqual(len(charts['booking_status']['labels']), 1)

    def test_audit_middleware_logs_authenticated_post(self):
        self.client.login(username='analyticscustomer', password='StrongPass123!')
        response = self.client.post(reverse('notifications:mark_all_read'))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(AuditLog.objects.filter(actor=self.customer, action__startswith='POST').exists())

# Create your tests here.
