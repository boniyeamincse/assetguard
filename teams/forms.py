from django import forms
from django.contrib.auth import get_user_model
from .models import Team

User = get_user_model()

class TeamForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_active=True).order_by('first_name', 'last_name'),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Team Members'
    )

    class Meta:
        model = Team
        fields = ('team_name', 'team_type', 'description', 'status', 'members')
        widgets = {
            'team_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Team Name'}),
            'team_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Team Description'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['team_name'].widget.attrs.update({'placeholder': 'Enter team name'})
