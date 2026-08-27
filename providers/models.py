from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from services.models import ServiceCategory


class ProviderProfile(models.Model):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    VERIFICATION_CHOICES = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='provider_profile')
    business_name = models.CharField(max_length=160)
    bio = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    service_area = models.CharField(max_length=160, db_index=True)
    base_location = models.CharField(max_length=160, db_index=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    profile_photo = models.ImageField(upload_to='providers/photos/', blank=True)
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_CHOICES, default=PENDING, db_index=True)
    emergency_available = models.BooleanField(default=False, db_index=True)
    response_rate = models.PositiveIntegerField(default=80, validators=[MaxValueValidator(100)])
    cancellation_rate = models.PositiveIntegerField(default=5, validators=[MaxValueValidator(100)])
    completed_jobs = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    trust_score = models.PositiveIntegerField(default=50, validators=[MinValueValidator(0), MaxValueValidator(100)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-trust_score', '-average_rating']
        indexes = [
            models.Index(fields=['verification_status', 'base_location']),
            models.Index(fields=['emergency_available', 'trust_score']),
        ]

    def __str__(self):
        return self.business_name

    @property
    def is_verified(self):
        return self.verification_status == self.APPROVED


class ProviderService(models.Model):
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE, related_name='services')
    category = models.ForeignKey(ServiceCategory, on_delete=models.PROTECT, related_name='provider_services')
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        unique_together = ('provider', 'category', 'title')
        indexes = [models.Index(fields=['category', 'starting_price'])]

    def __str__(self):
        return f'{self.title} by {self.provider}'


class VerificationDocument(models.Model):
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE, related_name='verification_documents')
    document_type = models.CharField(max_length=80)
    document = models.FileField(upload_to='verification/private/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

# Create your models here.
