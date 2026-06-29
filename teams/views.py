from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from .models import Team
from .forms import TeamForm

User = get_user_model()

class SuperAdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_super_admin()

    def handle_no_permission(self):
        return redirect('dashboard:dashboard')

class TeamListView(LoginRequiredMixin, ListView):
    model = Team
    template_name = 'teams/team_list.html'
    context_object_name = 'teams'
    paginate_by = 20

    def get_queryset(self):
        queryset = Team.objects.all().order_by('-created_at')
        search = self.request.GET.get('search', '')
        team_type = self.request.GET.get('type', '')
        status = self.request.GET.get('status', '')

        if search:
            queryset = queryset.filter(team_name__icontains=search)
        if team_type:
            queryset = queryset.filter(team_type=team_type)
        if status:
            queryset = queryset.filter(status=status)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_types'] = Team.TEAM_TYPE_CHOICES
        context['statuses'] = Team.STATUS_CHOICES
        context['current_search'] = self.request.GET.get('search', '')
        context['current_type'] = self.request.GET.get('type', '')
        context['current_status'] = self.request.GET.get('status', '')
        return context

class TeamDetailView(LoginRequiredMixin, DetailView):
    model = Team
    template_name = 'teams/team_detail.html'
    context_object_name = 'team'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['members'] = self.object.members.all()
        return context

class TeamCreateView(LoginRequiredMixin, SuperAdminRequiredMixin, CreateView):
    model = Team
    form_class = TeamForm
    template_name = 'teams/team_form.html'
    success_url = reverse_lazy('teams:team_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Team {form.instance.team_name} created successfully!')
        return response

class TeamUpdateView(LoginRequiredMixin, SuperAdminRequiredMixin, UpdateView):
    model = Team
    form_class = TeamForm
    template_name = 'teams/team_form.html'
    success_url = reverse_lazy('teams:team_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Team {form.instance.team_name} updated successfully!')
        return response

class TeamDeleteView(LoginRequiredMixin, SuperAdminRequiredMixin, DeleteView):
    model = Team
    template_name = 'teams/team_confirm_delete.html'
    success_url = reverse_lazy('teams:team_list')

    def delete(self, request, *args, **kwargs):
        team = self.get_object()
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'Team {team.team_name} deleted successfully!')
        return response

def add_team_member(request, team_id):
    if not request.user.is_super_admin():
        return redirect('dashboard:dashboard')

    team = get_object_or_404(Team, pk=team_id)

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, pk=user_id)

        if not team.members.filter(pk=user.pk).exists():
            team.members.add(user)
            messages.success(request, f'{user.get_full_name()} added to {team.team_name}')

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})

    return redirect('teams:team_detail', pk=team_id)

def remove_team_member(request, team_id, user_id):
    if not request.user.is_super_admin():
        return redirect('dashboard:dashboard')

    team = get_object_or_404(Team, pk=team_id)
    user = get_object_or_404(User, pk=user_id)

    if team.members.filter(pk=user.pk).exists():
        team.members.remove(user)
        messages.success(request, f'{user.get_full_name()} removed from {team.team_name}')

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})

    return redirect('teams:team_detail', pk=team_id)
