from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Team(models.Model):
    TEAM_TYPE_CHOICES = [
        ('security', 'Security Team'),
        ('software', 'Software Team'),
        ('management', 'Management Team'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    team_name = models.CharField(max_length=150, unique=True)
    team_type = models.CharField(max_length=50, choices=TEAM_TYPE_CHOICES)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    members = models.ManyToManyField(User, related_name='teams', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.team_name

    def member_count(self):
        return self.members.count()
