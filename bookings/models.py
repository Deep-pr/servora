from django.conf import settings
from django.db import models

from providers.models import ProviderProfile, ProviderService


class Booking(models.Model):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    CONFIRMED = 'confirmed'
    ON_THE_WAY = 'on_the_way'
    WORK_STARTED = 'work_started'
    COMPLETED = 'completed'
    REVIEWED = 'reviewed'
    REJECTED = 'rejected'
    CANCELLED = 'cancelled'
    RESCHEDULED = 'rescheduled'
    DISPUTED = 'disputed'
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (CONFIRMED, 'Confirmed'),
        (ON_THE_WAY, 'Provider On The Way'),
        (WORK_STARTED, 'Work Started'),
        (COMPLETED, 'Completed'),
        (REVIEWED, 'Reviewed'),
        (REJECTED, 'Rejected'),
        (CANCELLED, 'Cancelled'),
        (RESCHEDULED, 'Rescheduled'),
        (DISPUTED, 'Disputed'),
    )

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    provider = models.ForeignKey(ProviderProfile, on_delete=models.PROTECT, related_name='bookings')
    provider_service = models.ForeignKey(ProviderService, on_delete=models.PROTECT, related_name='bookings')
    scheduled_for = models.DateTimeField(db_index=True)
    address = models.TextField()
    problem_description = models.TextField()
    contact_preference = models.CharField(max_length=40, default='phone')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=PENDING, db_index=True)
    estimated_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-scheduled_for']
        indexes = [models.Index(fields=['customer', 'status']), models.Index(fields=['provider', 'status'])]

    def __str__(self):
        return f'{self.provider_service.title} for {self.customer}'


class Quote(models.Model):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    EXPIRED = 'expired'
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
        (EXPIRED, 'Expired'),
    )

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='quotes')
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE, related_name='quotes')
    estimated_price = models.DecimalField(max_digits=10, decimal_places=2)
    service_description = models.TextField()
    expected_completion_time = models.CharField(max_length=120)
    notes = models.TextField(blank=True)
    expires_at = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

# Create your models here.
