from django import forms
from .models import Vulnerability

class AssetVulnerabilityForm(forms.ModelForm):
    class Meta:
        model = Vulnerability
        fields = ['asset', 'title', 'description', 'bug_type', 'severity', 'priority', 'cvss_score', 'affected_url', 'affected_parameter', 'steps_to_reproduce', 'impact', 'recommendation', 'due_date', 'assigned_to', 'assigned_team']
        widgets = {
            'asset': forms.HiddenInput(),
        }
