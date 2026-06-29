from django.contrib import admin
from .models import Team

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'team_type', 'status', 'member_count', 'created_at')
    list_filter = ('team_type', 'status', 'created_at')
    search_fields = ('team_name', 'description')
    filter_horizontal = ('members',)
