from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('actor', 'action', 'target_model', 'target_id', 'created_at')
    list_filter = ('action', 'target_model', 'created_at')
    search_fields = ('actor__username', 'action', 'target_model', 'target_id')

# Register your models here.
