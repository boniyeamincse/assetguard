from django.urls import path
from . import views

app_name = 'vulnerabilities'

urlpatterns = [
    path('', views.VulnerabilityListView.as_view(), name='vulnerability_list'),
    path('create/', views.VulnerabilityCreateView.as_view(), name='vulnerability_create'),
    path('<int:pk>/', views.VulnerabilityDetailView.as_view(), name='vulnerability_detail'),
    path('<int:pk>/edit/', views.VulnerabilityUpdateView.as_view(), name='vulnerability_edit'),
    path('<int:pk>/assign/', views.vulnerability_assign, name='vulnerability_assign'),
    path('<int:pk>/update-status/', views.vulnerability_update_status, name='vulnerability_update_status'),
    path('<int:pk>/retest/', views.vulnerability_retest, name='vulnerability_retest'),
    path('<int:pk>/close/', views.vulnerability_close, name='vulnerability_close'),
    path('<int:pk>/reopen/', views.vulnerability_reopen, name='vulnerability_reopen'),
    path('<int:pk>/resolve/', views.resolve_bug, name='resolve_bug'),
    path('<int:pk>/reopen-bug/', views.reopen_bug, name='reopen_bug'),
    path('<int:pk>/mark-in-progress/', views.mark_in_progress, name='mark_in_progress'),
    path('<int:pk>/evidence/upload/', views.evidence_upload, name='evidence_upload'),
    path('evidence/<int:pk>/delete/', views.evidence_delete, name='evidence_delete'),
    path('<int:pk>/comments/add/', views.comment_add, name='comment_add'),
]
