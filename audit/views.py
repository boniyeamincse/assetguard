from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import AuditLog

class AuditLogListView(LoginRequiredMixin, ListView):
    model = AuditLog
    template_name = 'audit/audit_logs.html'
    context_object_name = 'logs'
    paginate_by = 50

    def get_queryset(self):
        if not self.request.user.is_super_admin():
            from django.http import HttpResponseForbidden
            raise HttpResponseForbidden()
        return AuditLog.objects.all().order_by('-created_at')
