from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.reports_index, name='reports_index'),
    path('assets/', views.asset_report, name='asset_report'),
    path('vulnerabilities/', views.vulnerability_report, name='vulnerability_report'),
    path('teams/', views.team_report, name='team_report'),
    path('overdue/', views.overdue_report, name='overdue_report'),
    path('export/csv/', views.export_csv, name='export_csv'),
    path('export/', views.export_reports, name='export_reports'),
    path('export/asset-pdf/', views.export_asset_report_pdf, name='export_asset_pdf'),
    path('export/vulnerability-pdf/', views.export_vulnerability_report_pdf, name='export_vuln_pdf'),
]
