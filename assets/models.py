from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from teams.models import Team

User = get_user_model()

class Asset(models.Model):
    ASSET_TYPE_CHOICES = [
        ('web_app', 'Web Application'),
        ('mobile_app', 'Mobile Application'),
        ('api', 'API'),
        ('database', 'Database'),
        ('server', 'Server'),
        ('network_device', 'Network Device'),
        ('desktop_app', 'Desktop Application'),
        ('cloud_service', 'Cloud Service'),
    ]

    CRITICALITY_CHOICES = [
        ('critical', 'Critical'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('retired', 'Retired'),
    ]

    asset_code = models.CharField(max_length=20, unique=True, editable=False)
    asset_name = models.CharField(max_length=200)
    domain = models.CharField(max_length=255, blank=True)
    request_id = models.CharField(max_length=100, blank=True)
    asset_type = models.CharField(max_length=50, choices=ASSET_TYPE_CHOICES)
    description = models.TextField(blank=True)
    business_owner = models.CharField(max_length=150, blank=True)
    project_owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='owned_assets')
    software_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='software_assets')
    security_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='security_assets')
    technology_stack = models.TextField(blank=True)
    production_url = models.URLField(blank=True)
    staging_url = models.URLField(blank=True)
    repository_url = models.URLField(blank=True)
    server_ip = models.CharField(max_length=50, blank=True)
    database_name = models.CharField(max_length=100, blank=True)
    criticality = models.CharField(max_length=20, choices=CRITICALITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_assets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.asset_code} - {self.asset_name}"

    def save(self, *args, **kwargs):
        if not self.asset_code:
            year = timezone.now().year
            last_asset = Asset.objects.filter(asset_code__startswith=f'AST-{year}').order_by('-asset_code').first()
            if last_asset:
                num = int(last_asset.asset_code.split('-')[-1]) + 1
            else:
                num = 1
            self.asset_code = f'AST-{year}-{num:04d}'
        super().save(*args, **kwargs)

    def get_vulnerability_count(self):
        return self.vulnerabilities.count()

    def get_open_vulnerability_count(self):
        return self.vulnerabilities.filter(status__in=['new', 'triaged', 'assigned', 'in_progress', 'reopened']).count()

    def get_closed_vulnerability_count(self):
        return self.vulnerabilities.filter(status__in=['closed', 'risk_accepted', 'auto_closed']).count()

    def get_in_progress_vulnerability_count(self):
        return self.vulnerabilities.filter(status='in_progress').count()

    def get_critical_vulnerability_count(self):
        return self.vulnerabilities.filter(severity='critical', status__in=['new', 'triaged', 'assigned', 'in_progress', 'reopened']).count()

    def calculate_risk_score(self):
        critical = self.vulnerabilities.filter(severity='critical', status__in=['new', 'triaged', 'assigned', 'in_progress', 'reopened']).count()
        high = self.vulnerabilities.filter(severity='high', status__in=['new', 'triaged', 'assigned', 'in_progress', 'reopened']).count()
        medium = self.vulnerabilities.filter(severity='medium', status__in=['new', 'triaged', 'assigned', 'in_progress', 'reopened']).count()
        low = self.vulnerabilities.filter(severity='low', status__in=['new', 'triaged', 'assigned', 'in_progress', 'reopened']).count()
        informational = self.vulnerabilities.filter(severity='informational', status__in=['new', 'triaged', 'assigned', 'in_progress', 'reopened']).count()

        score = (critical * 10) + (high * 7) + (medium * 4) + (low * 2) + (informational * 1)
        return score

    def get_risk_rating(self):
        score = self.calculate_risk_score()
        if score == 0:
            return 'Low Risk'
        elif score <= 10:
            return 'Low Risk'
        elif score <= 30:
            return 'Medium Risk'
        elif score <= 60:
            return 'High Risk'
        else:
            return 'Critical Risk'
