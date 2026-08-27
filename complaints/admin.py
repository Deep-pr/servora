from django.contrib import admin

from .models import Complaint


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('customer', 'category', 'status', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('customer__username', 'description', 'admin_notes')

# Register your models here.
