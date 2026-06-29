from django.core.management.base import BaseCommand
from django.utils import timezone
from vulnerabilities.models import Vulnerability
from notifications.services import notify_bug_auto_closed

class Command(BaseCommand):
    help = 'Auto-close bugs that have been resolved for 10 days'

    def handle(self, *args, **options):
        now = timezone.now()

        bugs_to_close = Vulnerability.objects.filter(
            status='waiting_for_auto_close',
            auto_close_at__lte=now,
            is_auto_closed=False
        )

        count = 0
        for bug in bugs_to_close:
            bug.status = 'auto_closed'
            bug.is_auto_closed = True
            bug.auto_closed_at = now
            bug.save()

            # Send notification to related users
            notify_bug_auto_closed(bug)

            count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully auto-closed {count} bugs')
        )
