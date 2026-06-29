from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Asset

class AssetListView(LoginRequiredMixin, ListView):
    model = Asset
    template_name = 'assets/asset_list.html'
    context_object_name = 'assets'
    paginate_by = 20

class AssetDetailView(LoginRequiredMixin, DetailView):
    model = Asset
    template_name = 'assets/asset_detail.html'
    context_object_name = 'asset'

class AssetCreateView(LoginRequiredMixin, CreateView):
    model = Asset
    template_name = 'assets/asset_form.html'
    fields = ['asset_name', 'domain', 'request_id', 'asset_type', 'description', 'business_owner', 'project_owner', 'software_team', 'security_team', 'technology_stack', 'production_url', 'staging_url', 'repository_url', 'server_ip', 'database_name', 'criticality', 'status']
    success_url = reverse_lazy('assets:asset_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class AssetUpdateView(LoginRequiredMixin, UpdateView):
    model = Asset
    template_name = 'assets/asset_form.html'
    fields = ['asset_name', 'domain', 'request_id', 'asset_type', 'description', 'business_owner', 'project_owner', 'software_team', 'security_team', 'technology_stack', 'production_url', 'staging_url', 'repository_url', 'server_ip', 'database_name', 'criticality', 'status']
    success_url = reverse_lazy('assets:asset_list')

class AssetDeleteView(LoginRequiredMixin, DeleteView):
    model = Asset
    template_name = 'assets/asset_confirm_delete.html'
    success_url = reverse_lazy('assets:asset_list')
