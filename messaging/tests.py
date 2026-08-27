from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notifications.models import Notification
from providers.models import ProviderProfile
from .models import Conversation, Message


class MessagingTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.customer = User.objects.create_user(username='messagecustomer', password='StrongPass123!')
        self.provider_user = User.objects.create_user(username='messageprovider', password='StrongPass123!', role=User.PROVIDER)
        self.provider = ProviderProfile.objects.create(
            user=self.provider_user,
            business_name='Message Provider',
            base_location='Tinsukia',
            service_area='Tinsukia',
            verification_status=ProviderProfile.APPROVED,
        )

    def test_customer_can_start_conversation_and_send_message(self):
        self.client.login(username='messagecustomer', password='StrongPass123!')
        response = self.client.get(reverse('messaging:start_provider', args=[self.provider.pk]))

        conversation = Conversation.objects.get()
        self.assertRedirects(response, reverse('messaging:detail', args=[conversation.pk]))

        response = self.client.post(reverse('messaging:detail', args=[conversation.pk]), {
            'body': 'Hello, are you available today?',
        })

        self.assertRedirects(response, reverse('messaging:detail', args=[conversation.pk]))
        self.assertTrue(Message.objects.filter(conversation=conversation, sender=self.customer).exists())
        self.assertTrue(Notification.objects.filter(user=self.provider_user, title='New message').exists())

# Create your tests here.
