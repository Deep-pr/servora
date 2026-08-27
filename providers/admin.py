from django.contrib import admin

from .models import ProviderProfile, ProviderService, VerificationDocument


class ProviderServiceInline(admin.TabularInline):
    model = ProviderService
    extra = 1


@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'verification_status', 'base_location', 'trust_score', 'average_rating')
    list_filter = ('verification_status', 'emergency_available', 'base_location')
    search_fields = ('business_name', 'user__username', 'base_location', 'service_area')
    inlines = [ProviderServiceInline]


@admin.register(VerificationDocument)
class VerificationDocumentAdmin(admin.ModelAdmin):
    list_display = ('provider', 'document_type', 'uploaded_at', 'reviewed_at')
    list_filter = ('document_type',)

# Register your models here.
