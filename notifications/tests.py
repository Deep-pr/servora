from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Notification


class NotificationTests(TestCase):
    def test_user_can_mark_notifications_read(self):
        User = get_user_model()
        user = User.objects.create_user(username='notifyuser', password='StrongPass123!')
        Notification.objects.create(user=user, title='Test', message='Unread notification')

        self.client.login(username='notifyuser', password='StrongPass123!')
        response = self.client.post(reverse('notifications:mark_all_read'))

        self.assertRedirects(response, reverse('notifications:list'))
        self.assertFalse(Notification.objects.filter(user=user, is_read=False).exists())

# Create your tests here.
