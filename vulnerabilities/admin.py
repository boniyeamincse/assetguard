from django.contrib import admin
from .models import Vulnerability, VulnerabilityComment, VulnerabilityEvidence, VulnerabilityStatusHistory, RetestResult

@admin.register(Vulnerability)
class VulnerabilityAdmin(admin.ModelAdmin):
    list_display = ('vulnerability_code', 'title', 'asset', 'severity', 'status', 'assigned_to', 'created_at')
    list_filter = ('severity', 'priority', 'status', 'bug_type', 'created_at')
    search_fields = ('vulnerability_code', 'title', 'description')
    readonly_fields = ('vulnerability_code', 'created_at', 'updated_at')
    fieldsets = (
        ('Identification', {'fields': ('vulnerability_code', 'title', 'asset', 'description')}),
        ('Classification', {'fields': ('bug_type', 'severity', 'priority')}),
        ('Details', {'fields': ('cvss_score', 'affected_url', 'affected_parameter', 'steps_to_reproduce', 'impact', 'recommendation')}),
        ('Assignment', {'fields': ('reported_by', 'assigned_to')}),
        ('Status & Dates', {'fields': ('status', 'due_date', 'fixed_at', 'closed_at')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )

@admin.register(VulnerabilityComment)
class VulnerabilityCommentAdmin(admin.ModelAdmin):
    list_display = ('vulnerability', 'user', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('vulnerability__vulnerability_code', 'comment')

@admin.register(VulnerabilityEvidence)
class VulnerabilityEvidenceAdmin(admin.ModelAdmin):
    list_display = ('vulnerability', 'file_name', 'file_type', 'uploaded_by', 'created_at')
    list_filter = ('file_type', 'created_at')
    search_fields = ('vulnerability__vulnerability_code', 'file_name')

@admin.register(VulnerabilityStatusHistory)
class VulnerabilityStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('vulnerability', 'old_status', 'new_status', 'changed_by', 'created_at')
    list_filter = ('new_status', 'created_at')
    search_fields = ('vulnerability__vulnerability_code',)

@admin.register(RetestResult)
class RetestResultAdmin(admin.ModelAdmin):
    list_display = ('vulnerability', 'result', 'retested_by', 'retest_date')
    list_filter = ('result', 'retest_date')
    search_fields = ('vulnerability__vulnerability_code',)
