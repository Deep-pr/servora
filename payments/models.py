from django.db import models

from bookings.models import Booking


class Payment(models.Model):
    PENDING = 'pending'
    SUCCESSFUL = 'successful'
    FAILED = 'failed'
    REFUNDED = 'refunded'
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (SUCCESSFUL, 'Successful'),
        (FAILED, 'Failed'),
        (REFUNDED, 'Refunded'),
    )

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING, db_index=True)
    gateway_name = models.CharField(max_length=80, blank=True)
    gateway_reference = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

# Create your models here.
