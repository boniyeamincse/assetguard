from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from teams.models import Team
from assets.models import Asset
from vulnerabilities.models import Vulnerability

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed database with demo data'

    def handle(self, *args, **options):
        # Create users
        users_data = [
            {'username': 'admin', 'email': 'admin@demo.com', 'password': '123456', 'role': 'super_admin', 'first_name': 'Admin', 'last_name': 'User'},
            {'username': 'security', 'email': 'security@demo.com', 'password': '123456', 'role': 'security_team', 'first_name': 'Security', 'last_name': 'Team'},
            {'username': 'software', 'email': 'software@demo.com', 'password': '123456', 'role': 'software_team', 'first_name': 'Software', 'last_name': 'Team'},
            {'username': 'owner', 'email': 'owner@demo.com', 'password': '123456', 'role': 'project_owner', 'first_name': 'Project', 'last_name': 'Owner'},
            {'username': 'management', 'email': 'management@demo.com', 'password': '123456', 'role': 'management_viewer', 'first_name': 'Management', 'last_name': 'Viewer'},
        ]

        for user_data in users_data:
            if not User.objects.filter(username=user_data['username']).exists():
                User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password'],
                    role=user_data['role'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                )
                self.stdout.write(self.style.SUCCESS(f"Created user: {user_data['username']}"))

        # Create teams
        teams_data = [
            {'team_name': 'Security Team Alpha', 'team_type': 'security', 'description': 'Primary security team'},
            {'team_name': 'Software Development', 'team_type': 'software', 'description': 'Development team'},
            {'team_name': 'Management', 'team_type': 'management', 'description': 'Management team'},
        ]

        for team_data in teams_data:
            if not Team.objects.filter(team_name=team_data['team_name']).exists():
                team = Team.objects.create(**team_data)
                team.members.add(User.objects.filter(role=team_data['team_type']).first())
                self.stdout.write(self.style.SUCCESS(f"Created team: {team_data['team_name']}"))

        # Create assets
        assets_data = [
            {'asset_name': 'ERP System', 'asset_type': 'web_app', 'criticality': 'critical', 'description': 'Enterprise Resource Planning System'},
            {'asset_name': 'HRM System', 'asset_type': 'web_app', 'criticality': 'high', 'description': 'Human Resource Management System'},
            {'asset_name': 'Payroll API', 'asset_type': 'api', 'criticality': 'critical', 'description': 'Payroll Processing API'},
            {'asset_name': 'Customer Portal', 'asset_type': 'web_app', 'criticality': 'medium', 'description': 'Customer Self Service Portal'},
        ]

        for asset_data in assets_data:
            if not Asset.objects.filter(asset_name=asset_data['asset_name']).exists():
                asset_data['created_by'] = User.objects.filter(role='super_admin').first()
                Asset.objects.create(**asset_data)
                self.stdout.write(self.style.SUCCESS(f"Created asset: {asset_data['asset_name']}"))

        self.stdout.write(self.style.SUCCESS("Seed data created successfully!"))
