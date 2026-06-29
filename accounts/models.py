from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('security_team', 'Security Team'),
        ('software_team', 'Software Team'),
        ('project_owner', 'Project Owner'),
        ('management_viewer', 'Management Viewer'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='security_team')
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

    def is_super_admin(self):
        return self.role == 'super_admin'

    def is_security_team(self):
        return self.role == 'security_team'

    def is_software_team(self):
        return self.role == 'software_team'

    def is_project_owner(self):
        return self.role == 'project_owner'

    def is_management_viewer(self):
        return self.role == 'management_viewer'
