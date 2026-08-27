from django.contrib import admin

from .models import Booking, Quote


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('provider_service', 'customer', 'provider', 'scheduled_for', 'status', 'estimated_amount')
    list_filter = ('status', 'scheduled_for')
    search_fields = ('customer__username', 'provider__business_name', 'address')


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('booking', 'provider', 'estimated_price', 'status', 'expires_at')
    list_filter = ('status', 'expires_at')

# Register your models here.
