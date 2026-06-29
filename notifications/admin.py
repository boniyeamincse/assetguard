from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'recipient', 'notification_type', 'priority', 'is_read', 'is_deleted', 'created_at')
    list_filter = ('notification_type', 'priority', 'is_read', 'is_deleted', 'created_at')
    search_fields = ('title', 'message', 'recipient__username')
    readonly_fields = ('created_at', 'read_at')
    fieldsets = (
        ('Notification', {'fields': ('recipient', 'sender', 'title', 'message')}),
        ('Classification', {'fields': ('notification_type', 'priority')}),
        ('Related Objects', {'fields': ('related_asset', 'related_vulnerability')}),
        ('Action', {'fields': ('action_url',)}),
        ('Status', {'fields': ('is_read', 'read_at', 'is_deleted')}),
        ('Timestamps', {'fields': ('created_at',)}),
    )
