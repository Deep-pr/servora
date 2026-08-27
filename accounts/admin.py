from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomerProfile, User


@admin.register(User)
class ServoraUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Servora role', {'fields': ('role', 'phone')}),
    )
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'created_at')
    search_fields = ('user__username', 'user__email', 'city')

# Register your models here.
