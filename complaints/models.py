from django.conf import settings
from django.db import models

from bookings.models import Booking


class Complaint(models.Model):
    OPEN = 'open'
    UNDER_REVIEW = 'under_review'
    RESOLVED = 'resolved'
    REJECTED = 'rejected'
    STATUS_CHOICES = (
        (OPEN, 'Open'),
        (UNDER_REVIEW, 'Under Review'),
        (RESOLVED, 'Resolved'),
        (REJECTED, 'Rejected'),
    )

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='complaints')
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True, related_name='complaints')
    category = models.CharField(max_length=80)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=OPEN, db_index=True)
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Create your models here.
