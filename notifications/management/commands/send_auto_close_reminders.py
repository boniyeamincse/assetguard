from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from vulnerabilities.models import Vulnerability
from notifications.services import notify_auto_close_reminder

class Command(BaseCommand):
    help = 'Send reminders to assigned users for bugs about to auto-close'

    def handle(self, *args, **options):
        tomorrow = timezone.now() + timedelta(days=1)
        tomorrow_start = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow_end = tomorrow_start + timedelta(days=1)

        bugs_to_remind = Vulnerability.objects.filter(
            status='waiting_for_auto_close',
            auto_close_at__gte=tomorrow_start,
            auto_close_at__lt=tomorrow_end,
            is_auto_closed=False
        )

        count = 0
        for bug in bugs_to_remind:
            notify_auto_close_reminder(bug)
            count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Sent {count} auto-close reminder notifications')
        )
