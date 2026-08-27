from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import ServiceCategory


class ServiceCategoryManagementTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.staff = User.objects.create_user(username='staff', password='StrongPass123!', is_staff=True)
        self.customer = User.objects.create_user(username='customer', password='StrongPass123!')

    def test_staff_can_create_category(self):
        self.client.login(username='staff', password='StrongPass123!')
        response = self.client.post(reverse('services:category_create'), {
            'name': 'Generator Repair',
            'slug': 'generator-repair',
            'icon': 'GEN',
            'description': 'Generator servicing and emergency repair.',
            'is_active': 'on',
        })

        self.assertRedirects(response, reverse('services:category_manage'))
        self.assertTrue(ServiceCategory.objects.filter(slug='generator-repair').exists())

    def test_non_staff_cannot_manage_categories(self):
        self.client.login(username='customer', password='StrongPass123!')
        response = self.client.get(reverse('services:category_manage'))
        self.assertEqual(response.status_code, 302)

# Create your tests here.
