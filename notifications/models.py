from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('bug_created', 'Bug Created'),
        ('bug_assigned', 'Bug Assigned'),
        ('bug_reassigned', 'Bug Reassigned'),
        ('bug_status_changed', 'Status Changed'),
        ('bug_resolved', 'Bug Resolved'),
        ('bug_waiting_auto_close', 'Waiting for Auto Close'),
        ('bug_auto_closed', 'Bug Auto Closed'),
        ('bug_reopened', 'Bug Reopened'),
        ('bug_closed', 'Bug Closed'),
        ('bug_overdue', 'Bug Overdue'),
        ('critical_bug_created', 'Critical Bug Created'),
        ('comment_added', 'Comment Added'),
        ('evidence_uploaded', 'Evidence Uploaded'),
        ('retest_required', 'Retest Required'),
        ('retest_failed', 'Retest Failed'),
        ('retest_passed', 'Retest Passed'),
        ('auto_close_reminder', 'Auto Close Reminder'),
        ('system_alert', 'System Alert'),
    ]

    PRIORITIES = [
        ('critical', 'Critical'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
        ('info', 'Info'),
    ]

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    priority = models.CharField(max_length=20, choices=PRIORITIES, default='info')
    title = models.CharField(max_length=200)
    message = models.TextField()
    related_asset = models.ForeignKey('assets.Asset', on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')
    related_vulnerability = models.ForeignKey('vulnerabilities.Vulnerability', on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')
    action_url = models.URLField(blank=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.recipient.username}"

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()

    def soft_delete(self):
        self.is_deleted = True
        self.save()
