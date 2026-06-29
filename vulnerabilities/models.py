from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from assets.models import Asset
from teams.models import Team

User = get_user_model()

class Vulnerability(models.Model):
    BUG_TYPE_CHOICES = [
        ('sql_injection', 'SQL Injection'),
        ('xss', 'Cross Site Scripting'),
        ('broken_access_control', 'Broken Access Control'),
        ('insecure_direct_object_reference', 'Insecure Direct Object Reference'),
        ('authentication_bypass', 'Authentication Bypass'),
        ('sensitive_data_exposure', 'Sensitive Data Exposure'),
        ('weak_password_policy', 'Weak Password Policy'),
        ('missing_rate_limit', 'Missing Rate Limit'),
        ('security_misconfiguration', 'Security Misconfiguration'),
        ('vulnerable_component', 'Vulnerable Component'),
        ('file_upload_vulnerability', 'File Upload Vulnerability'),
        ('business_logic_flaw', 'Business Logic Flaw'),
        ('api_security_issue', 'API Security Issue'),
        ('server_misconfiguration', 'Server Misconfiguration'),
        ('network_security_issue', 'Network Security Issue'),
        ('other', 'Other'),
    ]

    SEVERITY_CHOICES = [
        ('critical', 'Critical'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
        ('informational', 'Informational'),
    ]

    PRIORITY_CHOICES = [
        ('urgent', 'Urgent'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    STATUS_CHOICES = [
        ('new', 'New'),
        ('triaged', 'Triaged'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('fixed', 'Fixed'),
        ('ready_for_retest', 'Ready for Retest'),
        ('retesting', 'Retesting'),
        ('verified_fixed', 'Verified Fixed'),
        ('waiting_for_auto_close', 'Waiting for Auto Close'),
        ('auto_closed', 'Auto Closed'),
        ('closed', 'Closed'),
        ('reopened', 'Reopened'),
        ('rejected', 'Rejected'),
        ('risk_accepted', 'Risk Accepted'),
    ]

    vulnerability_code = models.CharField(max_length=20, unique=True, editable=False)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='vulnerabilities')
    title = models.CharField(max_length=300)
    description = models.TextField()
    bug_type = models.CharField(max_length=100, choices=BUG_TYPE_CHOICES)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='high')
    cvss_score = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    affected_url = models.URLField(blank=True)
    affected_parameter = models.CharField(max_length=300, blank=True)
    steps_to_reproduce = models.TextField(blank=True)
    impact = models.TextField(blank=True)
    recommendation = models.TextField(blank=True)
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reported_vulnerabilities')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_vulnerabilities')
    assigned_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_vulnerabilities_team')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='new')
    due_date = models.DateTimeField(null=True, blank=True)
    fixed_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_vulnerabilities')
    resolved_at = models.DateTimeField(null=True, blank=True)
    auto_close_at = models.DateTimeField(null=True, blank=True)
    auto_closed_at = models.DateTimeField(null=True, blank=True)
    is_auto_closed = models.BooleanField(default=False)
    resolution_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.vulnerability_code} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.vulnerability_code:
            year = timezone.now().year
            last_vuln = Vulnerability.objects.filter(vulnerability_code__startswith=f'VULN-{year}').order_by('-vulnerability_code').first()
            if last_vuln:
                num = int(last_vuln.vulnerability_code.split('-')[-1]) + 1
            else:
                num = 1
            self.vulnerability_code = f'VULN-{year}-{num:04d}'
        super().save(*args, **kwargs)

    def is_overdue(self):
        if self.status in ['closed', 'verified_fixed', 'risk_accepted', 'rejected']:
            return False
        if self.due_date:
            return self.due_date < timezone.now()
        return False

    def get_status_display_color(self):
        color_map = {
            'critical': 'danger',
            'high': 'warning',
            'medium': 'info',
            'low': 'success',
            'informational': 'secondary',
        }
        return color_map.get(self.severity, 'secondary')


class VulnerabilityComment(models.Model):
    vulnerability = models.ForeignKey(Vulnerability, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment on {self.vulnerability.vulnerability_code} by {self.user}"


class VulnerabilityEvidence(models.Model):
    vulnerability = models.ForeignKey(Vulnerability, on_delete=models.CASCADE, related_name='evidences')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to='evidences/%Y/%m/%d/')
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)
    file_size = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Evidence for {self.vulnerability.vulnerability_code}"


class VulnerabilityStatusHistory(models.Model):
    vulnerability = models.ForeignKey(Vulnerability, on_delete=models.CASCADE, related_name='status_history')
    old_status = models.CharField(max_length=50, blank=True)
    new_status = models.CharField(max_length=50)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.vulnerability.vulnerability_code}: {self.old_status} → {self.new_status}"


class RetestResult(models.Model):
    RESULT_CHOICES = [
        ('passed', 'Passed'),
        ('failed', 'Failed'),
        ('partially_fixed', 'Partially Fixed'),
    ]

    vulnerability = models.ForeignKey(Vulnerability, on_delete=models.CASCADE, related_name='retest_results')
    retested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    result = models.CharField(max_length=50, choices=RESULT_CHOICES)
    note = models.TextField(blank=True)
    retest_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Retest for {self.vulnerability.vulnerability_code}: {self.get_result_display()}"
