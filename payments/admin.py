from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'status', 'gateway_name', 'created_at')
    list_filter = ('status', 'gateway_name')

# Register your models here.
