from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.db.models import Q
from .forms import UserCreationForm, UserUpdateForm

User = get_user_model()

@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.phone = request.POST.get('phone', user.phone)
        user.department = request.POST.get('department', user.department)
        user.designation = request.POST.get('designation', user.designation)

        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']

        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:profile')

    return render(request, 'accounts/profile.html', {'user': user})

class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('accounts:profile')

@login_required
def change_password(request):
    if request.method == 'POST':
        from django.contrib.auth.forms import PasswordChangeForm
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            from django.contrib.auth import update_session_auth_hash
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('accounts:profile')
    else:
        from django.contrib.auth.forms import PasswordChangeForm
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})

class SuperAdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_super_admin()

    def handle_no_permission(self):
        return redirect('dashboard:dashboard')

class UserListView(LoginRequiredMixin, SuperAdminRequiredMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 20

    def get_queryset(self):
        queryset = User.objects.all().order_by('-created_at')

        search = self.request.GET.get('search', '')
        role_filter = self.request.GET.get('role', '')
        status_filter = self.request.GET.get('status', '')
        active_filter = self.request.GET.get('active', '')

        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )

        if role_filter:
            queryset = queryset.filter(role=role_filter)

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        if active_filter:
            if active_filter == 'active':
                queryset = queryset.filter(is_active=True)
            elif active_filter == 'inactive':
                queryset = queryset.filter(is_active=False)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role_choices'] = User.ROLE_CHOICES
        context['status_choices'] = User.STATUS_CHOICES
        context['current_search'] = self.request.GET.get('search', '')
        context['current_role'] = self.request.GET.get('role', '')
        context['current_status'] = self.request.GET.get('status', '')
        context['current_active'] = self.request.GET.get('active', '')
        return context

class UserDetailView(LoginRequiredMixin, SuperAdminRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/user_detail.html'
    context_object_name = 'user_obj'

class UserCreateView(LoginRequiredMixin, SuperAdminRequiredMixin, CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'User {form.instance.get_full_name()} created successfully!')
        return response

class UserUpdateView(LoginRequiredMixin, SuperAdminRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'User {form.instance.get_full_name()} updated successfully!')
        return response

class UserDeleteView(LoginRequiredMixin, SuperAdminRequiredMixin, DeleteView):
    model = User
    template_name = 'accounts/user_confirm_delete.html'
    success_url = reverse_lazy('accounts:user_list')

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'User {user.get_full_name()} deleted successfully!')
        return response

@login_required
def user_activate(request, pk):
    if not request.user.is_super_admin():
        return redirect('dashboard:dashboard')

    user = get_object_or_404(User, pk=pk)
    user.is_active = True
    user.save()
    messages.success(request, f'User {user.get_full_name()} activated.')
    return redirect('accounts:user_detail', pk=pk)

@login_required
def user_deactivate(request, pk):
    if not request.user.is_super_admin():
        return redirect('dashboard:dashboard')

    user = get_object_or_404(User, pk=pk)
    user.is_active = False
    user.save()
    messages.success(request, f'User {user.get_full_name()} deactivated.')
    return redirect('accounts:user_detail', pk=pk)
