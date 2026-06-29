from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'module_name', 'record_id', 'ip_address', 'created_at')
    list_filter = ('action', 'module_name', 'created_at')
    search_fields = ('user__username', 'action', 'module_name')
    readonly_fields = ('created_at', 'user', 'action', 'module_name', 'record_id', 'old_value', 'new_value', 'ip_address', 'user_agent')
