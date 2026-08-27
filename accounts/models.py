from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    CUSTOMER = 'customer'
    PROVIDER = 'provider'
    ADMIN = 'admin'
    ROLE_CHOICES = (
        (CUSTOMER, 'Customer'),
        (PROVIDER, 'Service Provider'),
        (ADMIN, 'Administrator'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=CUSTOMER, db_index=True)
    phone = models.CharField(max_length=20, blank=True)

    def is_customer(self):
        return self.role == self.CUSTOMER

    def is_provider(self):
        return self.role == self.PROVIDER


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True, db_index=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.get_full_name() or self.user.username} profile'

# Create your models here.
