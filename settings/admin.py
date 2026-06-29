from django.contrib import admin
from .models import SystemSetting

@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'setting_type', 'is_editable', 'updated_at')
    list_filter = ('setting_type', 'is_editable')
    search_fields = ('key', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Setting Information', {'fields': ('key', 'value', 'description')}),
        ('Configuration', {'fields': ('setting_type', 'is_editable')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
