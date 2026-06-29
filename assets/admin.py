from django.contrib import admin
from .models import Asset

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('asset_code', 'asset_name', 'asset_type', 'criticality', 'status', 'created_at')
    list_filter = ('asset_type', 'criticality', 'status', 'created_at')
    search_fields = ('asset_code', 'asset_name', 'description')
    readonly_fields = ('asset_code', 'created_at', 'updated_at')
    fieldsets = (
        ('Asset Information', {'fields': ('asset_code', 'asset_name', 'asset_type', 'description')}),
        ('Ownership', {'fields': ('business_owner', 'project_owner', 'software_team', 'security_team')}),
        ('URLs & Access', {'fields': ('production_url', 'staging_url', 'repository_url', 'server_ip', 'database_name')}),
        ('Technical Details', {'fields': ('technology_stack',)}),
        ('Status', {'fields': ('criticality', 'status')}),
        ('Timestamps', {'fields': ('created_by', 'created_at', 'updated_at')}),
    )
