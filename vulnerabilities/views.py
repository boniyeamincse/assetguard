from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Vulnerability, VulnerabilityComment, VulnerabilityEvidence, VulnerabilityStatusHistory, RetestResult

class VulnerabilityListView(LoginRequiredMixin, ListView):
    model = Vulnerability
    template_name = 'vulnerabilities/vulnerability_list.html'
    context_object_name = 'vulnerabilities'
    paginate_by = 20

    def get_queryset(self):
        queryset = Vulnerability.objects.all().order_by('-created_at')
        filter_type = self.request.GET.get('filter', 'all')

        if filter_type == 'open':
            queryset = queryset.filter(status__in=['new', 'assigned', 'in_progress', 'reopened'])
        elif filter_type == 'assigned-to-me':
            queryset = queryset.filter(assigned_to=self.request.user)
        elif filter_type == 'waiting':
            queryset = queryset.filter(status='waiting_for_auto_close')
        elif filter_type == 'auto-closed':
            queryset = queryset.filter(status='auto_closed')
        elif filter_type == 'closed':
            queryset = queryset.filter(status='closed')
        elif filter_type == 'reopened':
            queryset = queryset.filter(status='reopened')

        return queryset

class VulnerabilityDetailView(LoginRequiredMixin, DetailView):
    model = Vulnerability
    template_name = 'vulnerabilities/vulnerability_detail.html'
    context_object_name = 'vulnerability'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from django.contrib.auth import get_user_model
        from teams.models import Team
        User = get_user_model()
        context['users'] = User.objects.filter(is_active=True).order_by('first_name', 'username')
        context['teams'] = Team.objects.all().order_by('team_name')
        return context

class VulnerabilityCreateView(LoginRequiredMixin, CreateView):
    model = Vulnerability
    template_name = 'vulnerabilities/vulnerability_form.html'
    fields = ['asset', 'title', 'description', 'bug_type', 'severity', 'priority', 'cvss_score', 'affected_url', 'affected_parameter', 'steps_to_reproduce', 'impact', 'recommendation', 'due_date', 'assigned_to', 'assigned_team']
    success_url = reverse_lazy('vulnerabilities:vulnerability_list')

    def form_valid(self, form):
        form.instance.reported_by = self.request.user
        form.instance.status = 'new'
        response = super().form_valid(form)

        # Notify if critical bug is created
        if form.instance.severity == 'critical':
            from notifications.services import notify_critical_bug_created
            notify_critical_bug_created(form.instance, self.request.user)

        return response

class AssetVulnerabilityCreateView(LoginRequiredMixin, CreateView):
    model = Vulnerability
    template_name = 'vulnerabilities/vulnerability_form.html'
    from .forms import AssetVulnerabilityForm
    form_class = AssetVulnerabilityForm

    def get_initial(self):
        initial = super().get_initial()
        initial['asset'] = self.kwargs.get('asset_id')
        return initial

    def form_valid(self, form):
        form.instance.reported_by = self.request.user
        form.instance.status = 'new'
        # ensure the asset is strictly set to the URL kwarg
        form.instance.asset_id = self.kwargs.get('asset_id')
        return super().form_valid(form)

    def get_success_url(self):
        from django.urls import reverse
        return reverse('assets:asset_detail', kwargs={'pk': self.kwargs.get('asset_id')})


class VulnerabilityUpdateView(LoginRequiredMixin, UpdateView):
    model = Vulnerability
    template_name = 'vulnerabilities/vulnerability_form.html'
    fields = ['asset', 'title', 'description', 'bug_type', 'severity', 'priority', 'cvss_score', 'affected_url', 'affected_parameter', 'steps_to_reproduce', 'impact', 'recommendation', 'due_date', 'assigned_to', 'assigned_team']
    success_url = reverse_lazy('vulnerabilities:vulnerability_list')

@login_required
def vulnerability_assign(request, pk):
    vulnerability = get_object_or_404(Vulnerability, pk=pk)
    if request.method == 'POST':
        assigned_to_id = request.POST.get('assigned_to')
        assigned_team_id = request.POST.get('assigned_team')
        
        changed = False
        note_parts = []

        if assigned_to_id:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            assigned_to = get_object_or_404(User, pk=assigned_to_id)
            vulnerability.assigned_to = assigned_to
            changed = True
            note_parts.append(f'User: {assigned_to.get_full_name()}')
            
        if assigned_team_id:
            from teams.models import Team
            assigned_team = get_object_or_404(Team, pk=assigned_team_id)
            vulnerability.assigned_team = assigned_team
            changed = True
            note_parts.append(f'Team: {assigned_team.team_name}')

        if changed:
            vulnerability.status = 'assigned'
            vulnerability.save()
            VulnerabilityStatusHistory.objects.create(
                vulnerability=vulnerability,
                old_status='new',
                new_status='assigned',
                changed_by=request.user,
                note=f'Assigned to {", ".join(note_parts)}'
            )

            # Send notification to assigned user
            if vulnerability.assigned_to:
                from notifications.services import notify_bug_assigned
                notify_bug_assigned(vulnerability, vulnerability.assigned_to, request.user)

    return redirect('vulnerabilities:vulnerability_detail', pk=pk)

@login_required
def vulnerability_update_status(request, pk):
    vulnerability = get_object_or_404(Vulnerability, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status:
            VulnerabilityStatusHistory.objects.create(
                vulnerability=vulnerability,
                old_status=vulnerability.status,
                new_status=new_status,
                changed_by=request.user,
            )
            vulnerability.status = new_status
            if new_status == 'fixed':
                vulnerability.fixed_at = timezone.now()
            elif new_status == 'closed':
                vulnerability.closed_at = timezone.now()
            vulnerability.save()
    return redirect('vulnerabilities:vulnerability_detail', pk=pk)

@login_required
def vulnerability_retest(request, pk):
    vulnerability = get_object_or_404(Vulnerability, pk=pk)
    if request.method == 'POST':
        result = request.POST.get('result')
        note = request.POST.get('note', '')
        if result:
            RetestResult.objects.create(
                vulnerability=vulnerability,
                retested_by=request.user,
                result=result,
                note=note
            )
            if result == 'passed':
                vulnerability.status = 'verified_fixed'
                vulnerability.closed_at = timezone.now()
            elif result == 'failed':
                vulnerability.status = 'reopened'
            vulnerability.save()
            VulnerabilityStatusHistory.objects.create(
                vulnerability=vulnerability,
                old_status='retesting',
                new_status=vulnerability.status,
                changed_by=request.user,
                note=f'Retest result: {result}'
            )
    return redirect('vulnerabilities:vulnerability_detail', pk=pk)

@login_required
def vulnerability_close(request, pk):
    vulnerability = get_object_or_404(Vulnerability, pk=pk)
    vulnerability.status = 'closed'
    vulnerability.closed_at = timezone.now()
    vulnerability.save()
    VulnerabilityStatusHistory.objects.create(
        vulnerability=vulnerability,
        old_status='verified_fixed',
        new_status='closed',
        changed_by=request.user,
    )
    return redirect('vulnerabilities:vulnerability_detail', pk=pk)

@login_required
def vulnerability_reopen(request, pk):
    vulnerability = get_object_or_404(Vulnerability, pk=pk)
    vulnerability.status = 'reopened'
    vulnerability.save()
    VulnerabilityStatusHistory.objects.create(
        vulnerability=vulnerability,
        old_status='closed',
        new_status='reopened',
        changed_by=request.user,
    )
    return redirect('vulnerabilities:vulnerability_detail', pk=pk)

@login_required
def resolve_bug(request, pk):
    vulnerability = get_object_or_404(Vulnerability, pk=pk)

    if request.user != vulnerability.assigned_to and not (request.user.is_super_admin() or request.user.is_software_team()):
        return redirect('vulnerabilities:vulnerability_detail', pk=pk)

    if request.method == 'POST':
        resolution_note = request.POST.get('resolution_note', '')
        now = timezone.now()

        old_status = vulnerability.status
        vulnerability.status = 'waiting_for_auto_close'
        vulnerability.resolved_by = request.user
        vulnerability.resolved_at = now
        vulnerability.auto_close_at = now + timezone.timedelta(days=10)
        vulnerability.resolution_note = resolution_note
        vulnerability.save()

        VulnerabilityStatusHistory.objects.create(
            vulnerability=vulnerability,
            old_status=old_status,
            new_status='waiting_for_auto_close',
            changed_by=request.user,
            note=f'Resolved by {request.user.get_full_name()}'
        )

        # Send notification to reporter and project owner
        from notifications.services import notify_bug_resolved
        notify_bug_resolved(vulnerability, request.user)

    return redirect('vulnerabilities:vulnerability_detail', pk=pk)

@login_required
def reopen_bug(request, pk):
    vulnerability = get_object_or_404(Vulnerability, pk=pk)

    if not (request.user.is_super_admin() or request.user.is_security_team() or
            (vulnerability.asset.project_owner == request.user)):
        return redirect('vulnerabilities:vulnerability_detail', pk=pk)

    old_status = vulnerability.status
    vulnerability.status = 'reopened'
    vulnerability.resolved_by = None
    vulnerability.resolved_at = None
    vulnerability.auto_close_at = None
    vulnerability.auto_closed_at = None
    vulnerability.is_auto_closed = False
    vulnerability.resolution_note = ''
    vulnerability.save()

    VulnerabilityStatusHistory.objects.create(
        vulnerability=vulnerability,
        old_status=old_status,
        new_status='reopened',
        changed_by=request.user,
        note=f'Reopened by {request.user.get_full_name()}'
    )

    # Send notification to assigned user
    from notifications.services import notify_bug_reopened
    notify_bug_reopened(vulnerability, request.user)

    return redirect('vulnerabilities:vulnerability_detail', pk=pk)

@login_required
def mark_in_progress(request, pk):
    vulnerability = get_object_or_404(Vulnerability, pk=pk)

    if request.user != vulnerability.assigned_to and not request.user.is_super_admin():
        return redirect('vulnerabilities:vulnerability_detail', pk=pk)

    if vulnerability.status not in ['assigned', 'reopened']:
        return redirect('vulnerabilities:vulnerability_detail', pk=pk)

    old_status = vulnerability.status
    vulnerability.status = 'in_progress'
    vulnerability.save()

    VulnerabilityStatusHistory.objects.create(
        vulnerability=vulnerability,
        old_status=old_status,
        new_status='in_progress',
        changed_by=request.user,
        note=f'Marked in progress by {request.user.get_full_name()}'
    )

    return redirect('vulnerabilities:vulnerability_detail', pk=pk)

@login_required
def evidence_upload(request, pk):
    vulnerability = get_object_or_404(Vulnerability, pk=pk)
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            evidence = VulnerabilityEvidence.objects.create(
                vulnerability=vulnerability,
                uploaded_by=request.user,
                file=file,
                file_name=file.name,
                file_type=file.content_type,
                file_size=file.size
            )
    return redirect('vulnerabilities:vulnerability_detail', pk=pk)

@login_required
def evidence_delete(request, pk):
    evidence = get_object_or_404(VulnerabilityEvidence, pk=pk)
    vulnerability_pk = evidence.vulnerability.pk
    evidence.delete()
    return redirect('vulnerabilities:vulnerability_detail', pk=vulnerability_pk)

@login_required
def comment_add(request, pk):
    vulnerability = get_object_or_404(Vulnerability, pk=pk)
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        if comment_text:
            VulnerabilityComment.objects.create(
                vulnerability=vulnerability,
                user=request.user,
                comment=comment_text
            )
    return redirect('vulnerabilities:vulnerability_detail', pk=pk)
