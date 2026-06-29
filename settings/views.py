from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
import psutil
import os

from .models import SystemSetting
from django.contrib.auth import get_user_model

User = get_user_model()

class SuperAdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_super_admin()

    def handle_no_permission(self):
        return redirect('dashboard:dashboard')

@login_required
def settings_index(request):
    """Settings main page"""
    if not request.user.is_super_admin():
        return redirect('dashboard:dashboard')
    return redirect('settings:general_settings')

@login_required
def general_settings(request):
    """General system settings"""
    if not request.user.is_super_admin():
        return redirect('dashboard:dashboard')

    if request.method == 'POST':
        app_name = request.POST.get('app_name', 'AssetGuard')
        app_version = request.POST.get('app_version', '2.0')
        organization = request.POST.get('organization', '')
        support_email = request.POST.get('support_email', '')

        # Update or create settings
        SystemSetting.objects.update_or_create(
            key='app_name',
            defaults={'value': app_name, 'setting_type': 'string', 'description': 'Application name'}
        )
        SystemSetting.objects.update_or_create(
            key='app_version',
            defaults={'value': app_version, 'setting_type': 'string', 'description': 'Application version'}
        )
        SystemSetting.objects.update_or_create(
            key='organization',
            defaults={'value': organization, 'setting_type': 'string', 'description': 'Organization name'}
        )
        SystemSetting.objects.update_or_create(
            key='support_email',
            defaults={'value': support_email, 'setting_type': 'string', 'description': 'Support email'}
        )

        messages.success(request, 'Settings updated successfully!')
        return redirect('settings:general_settings')

    settings_dict = {s.key: s.value for s in SystemSetting.objects.all()}

    context = {
        'app_name': settings_dict.get('app_name', 'AssetGuard'),
        'app_version': settings_dict.get('app_version', '2.0'),
        'organization': settings_dict.get('organization', ''),
        'support_email': settings_dict.get('support_email', ''),
        'current_user': request.user,
    }

    return render(request, 'settings/general_settings.html', context)

@login_required
def server_monitor(request):
    """Server monitoring page"""
    if not request.user.is_super_admin():
        return redirect('dashboard:dashboard')

    # Get system information
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    # Database statistics
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    last_hour_logins = User.objects.filter(last_login__gte=timezone.now() - timedelta(hours=1)).count()

    context = {
        'cpu_percent': cpu_percent,
        'memory_percent': memory.percent,
        'memory_available_gb': memory.available / (1024**3),
        'memory_total_gb': memory.total / (1024**3),
        'disk_percent': disk.percent,
        'disk_free_gb': disk.free / (1024**3),
        'disk_total_gb': disk.total / (1024**3),
        'total_users': total_users,
        'active_users': active_users,
        'last_hour_logins': last_hour_logins,
        'python_version': __import__('sys').version.split()[0],
        'server_uptime': timezone.now(),
    }

    return render(request, 'settings/server_monitor.html', context)

@login_required
def notification_settings(request):
    """Notification settings"""
    if not request.user.is_super_admin():
        return redirect('dashboard:dashboard')

    if request.method == 'POST':
        enable_email = request.POST.get('enable_email') == 'on'
        enable_system = request.POST.get('enable_system') == 'on'
        critical_threshold = request.POST.get('critical_threshold', '7')

        SystemSetting.objects.update_or_create(
            key='enable_email_notifications',
            defaults={'value': str(enable_email), 'setting_type': 'boolean'}
        )
        SystemSetting.objects.update_or_create(
            key='enable_system_notifications',
            defaults={'value': str(enable_system), 'setting_type': 'boolean'}
        )
        SystemSetting.objects.update_or_create(
            key='critical_bug_threshold_days',
            defaults={'value': critical_threshold, 'setting_type': 'integer'}
        )

        messages.success(request, 'Notification settings updated!')
        return redirect('settings:notification_settings')

    settings_dict = {s.key: s.value for s in SystemSetting.objects.all()}

    context = {
        'enable_email': settings_dict.get('enable_email_notifications', 'True') == 'True',
        'enable_system': settings_dict.get('enable_system_notifications', 'True') == 'True',
        'critical_threshold': settings_dict.get('critical_bug_threshold_days', '7'),
    }

    return render(request, 'settings/notification_settings.html', context)

@login_required
def security_settings(request):
    """Security and access control settings"""
    if not request.user.is_super_admin():
        return redirect('dashboard:dashboard')

    if request.method == 'POST':
        session_timeout = request.POST.get('session_timeout', '3600')
        force_https = request.POST.get('force_https') == 'on'
        allow_registration = request.POST.get('allow_registration') == 'on'

        SystemSetting.objects.update_or_create(
            key='session_timeout_seconds',
            defaults={'value': session_timeout, 'setting_type': 'integer'}
        )
        SystemSetting.objects.update_or_create(
            key='force_https',
            defaults={'value': str(force_https), 'setting_type': 'boolean'}
        )
        SystemSetting.objects.update_or_create(
            key='allow_user_registration',
            defaults={'value': str(allow_registration), 'setting_type': 'boolean'}
        )

        messages.success(request, 'Security settings updated!')
        return redirect('settings:security_settings')

    settings_dict = {s.key: s.value for s in SystemSetting.objects.all()}

    context = {
        'session_timeout': settings_dict.get('session_timeout_seconds', '3600'),
        'force_https': settings_dict.get('force_https', 'False') == 'True',
        'allow_registration': settings_dict.get('allow_user_registration', 'False') == 'True',
    }

    return render(request, 'settings/security_settings.html', context)
