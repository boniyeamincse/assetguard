from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from assets.models import Asset
from vulnerabilities.models import Vulnerability
from django.utils import timezone

@login_required
def dashboard(request):
    total_assets = Asset.objects.count()
    total_vulnerabilities = Vulnerability.objects.count()
    critical_open = Vulnerability.objects.filter(severity='critical', status__in=['new', 'triaged', 'assigned', 'in_progress', 'reopened']).count()
    high_open = Vulnerability.objects.filter(severity='high', status__in=['new', 'triaged', 'assigned', 'in_progress', 'reopened']).count()
    medium_open = Vulnerability.objects.filter(severity='medium', status__in=['new', 'triaged', 'assigned', 'in_progress', 'reopened']).count()
    low_open = Vulnerability.objects.filter(severity='low', status__in=['new', 'triaged', 'assigned', 'in_progress', 'reopened']).count()
    retest_pending = Vulnerability.objects.filter(status='ready_for_retest').count()
    overdue = Vulnerability.objects.filter(due_date__lt=timezone.now(), status__in=['new', 'triaged', 'assigned', 'in_progress', 'reopened']).count()
    closed = Vulnerability.objects.filter(status='closed').count()
    risk_accepted = Vulnerability.objects.filter(status='risk_accepted').count()

    recent_vulnerabilities = Vulnerability.objects.all()[:10]
    top_risky_assets = Asset.objects.all()[:5]

    context = {
        'total_assets': total_assets,
        'total_vulnerabilities': total_vulnerabilities,
        'critical_open': critical_open,
        'high_open': high_open,
        'medium_open': medium_open,
        'low_open': low_open,
        'retest_pending': retest_pending,
        'overdue': overdue,
        'closed': closed,
        'risk_accepted': risk_accepted,
        'recent_vulnerabilities': recent_vulnerabilities,
        'top_risky_assets': top_risky_assets,
    }

    return render(request, 'dashboard/dashboard.html', context)
