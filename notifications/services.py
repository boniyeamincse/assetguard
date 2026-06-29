from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Notification

User = get_user_model()

def create_notification(recipient, notification_type, title, message, sender=None, priority='info',
                       related_asset=None, related_vulnerability=None, action_url=None):
    """Create a new notification"""
    return Notification.objects.create(
        recipient=recipient,
        sender=sender,
        notification_type=notification_type,
        priority=priority,
        title=title,
        message=message,
        related_asset=related_asset,
        related_vulnerability=related_vulnerability,
        action_url=action_url
    )

def notify_bug_assigned(vulnerability, assigned_to, sender):
    """Notify user when bug is assigned"""
    title = f"Bug Assigned: {vulnerability.vulnerability_code}"
    message = f"You have been assigned to bug {vulnerability.vulnerability_code}: {vulnerability.title}"
    action_url = f"/vulnerabilities/{vulnerability.pk}/"

    create_notification(
        recipient=assigned_to,
        notification_type='bug_assigned',
        title=title,
        message=message,
        sender=sender,
        priority='high',
        related_vulnerability=vulnerability,
        action_url=action_url
    )

def notify_bug_resolved(vulnerability, sender):
    """Notify reporter and project owner when bug is resolved"""
    title = f"Bug Resolved: {vulnerability.vulnerability_code}"
    message = f"Bug {vulnerability.vulnerability_code} has been resolved and is waiting for auto-close."
    action_url = f"/vulnerabilities/{vulnerability.pk}/"

    # Notify reporter
    if vulnerability.reported_by and vulnerability.reported_by != sender:
        create_notification(
            recipient=vulnerability.reported_by,
            notification_type='bug_resolved',
            title=title,
            message=message,
            sender=sender,
            priority='medium',
            related_vulnerability=vulnerability,
            action_url=action_url
        )

    # Notify project owner
    if vulnerability.asset.project_owner and vulnerability.asset.project_owner != sender:
        create_notification(
            recipient=vulnerability.asset.project_owner,
            notification_type='bug_resolved',
            title=title,
            message=message,
            sender=sender,
            priority='medium',
            related_asset=vulnerability.asset,
            related_vulnerability=vulnerability,
            action_url=action_url
        )

def notify_bug_reopened(vulnerability, sender):
    """Notify assigned user when bug is reopened"""
    if vulnerability.assigned_to and vulnerability.assigned_to != sender:
        title = f"Bug Reopened: {vulnerability.vulnerability_code}"
        message = f"Bug {vulnerability.vulnerability_code} has been reopened. Please address the issues."
        action_url = f"/vulnerabilities/{vulnerability.pk}/"

        create_notification(
            recipient=vulnerability.assigned_to,
            notification_type='bug_reopened',
            title=title,
            message=message,
            sender=sender,
            priority='high',
            related_vulnerability=vulnerability,
            action_url=action_url
        )

def notify_bug_auto_closed(vulnerability):
    """Notify related users when bug is auto-closed"""
    title = f"Bug Auto Closed: {vulnerability.vulnerability_code}"
    message = f"Bug {vulnerability.vulnerability_code} has been automatically closed after 10 days."
    action_url = f"/vulnerabilities/{vulnerability.pk}/"

    # Notify reporter
    if vulnerability.reported_by:
        create_notification(
            recipient=vulnerability.reported_by,
            notification_type='bug_auto_closed',
            title=title,
            message=message,
            priority='info',
            related_vulnerability=vulnerability,
            action_url=action_url
        )

    # Notify assigned user
    if vulnerability.assigned_to:
        create_notification(
            recipient=vulnerability.assigned_to,
            notification_type='bug_auto_closed',
            title=title,
            message=message,
            priority='info',
            related_vulnerability=vulnerability,
            action_url=action_url
        )

    # Notify project owner
    if vulnerability.asset.project_owner:
        create_notification(
            recipient=vulnerability.asset.project_owner,
            notification_type='bug_auto_closed',
            title=title,
            message=message,
            priority='info',
            related_asset=vulnerability.asset,
            related_vulnerability=vulnerability,
            action_url=action_url
        )

def notify_critical_bug_created(vulnerability, sender):
    """Notify super admins, security team, and management when critical bug is created"""
    title = f"CRITICAL BUG CREATED: {vulnerability.vulnerability_code}"
    message = f"Critical bug detected in {vulnerability.asset.asset_name}: {vulnerability.title}"
    action_url = f"/vulnerabilities/{vulnerability.pk}/"

    # Get all super admins and security team members
    super_admins = User.objects.filter(role='super_admin', is_active=True)
    security_team = User.objects.filter(role='security_team', is_active=True)
    management = User.objects.filter(role='management_viewer', is_active=True)

    recipients = list(super_admins) + list(security_team) + list(management)

    for recipient in recipients:
        if recipient != sender:
            create_notification(
                recipient=recipient,
                notification_type='critical_bug_created',
                title=title,
                message=message,
                sender=sender,
                priority='critical',
                related_asset=vulnerability.asset,
                related_vulnerability=vulnerability,
                action_url=action_url
            )

def notify_auto_close_reminder(vulnerability):
    """Send reminder to assigned user before auto-close"""
    if vulnerability.assigned_to:
        title = f"Auto-Close Reminder: {vulnerability.vulnerability_code}"
        message = f"Bug {vulnerability.vulnerability_code} will be automatically closed tomorrow at {vulnerability.auto_close_at.strftime('%H:%M')} if not reopened."
        action_url = f"/vulnerabilities/{vulnerability.pk}/"

        create_notification(
            recipient=vulnerability.assigned_to,
            notification_type='auto_close_reminder',
            title=title,
            message=message,
            priority='medium',
            related_vulnerability=vulnerability,
            action_url=action_url
        )
