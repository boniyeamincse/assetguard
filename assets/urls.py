from django.urls import path
from . import views

app_name = 'assets'

from vulnerabilities.views import AssetVulnerabilityCreateView

urlpatterns = [
    path('<int:asset_id>/bugs/create/', AssetVulnerabilityCreateView.as_view(), name='asset_bug_create'),
    path('', views.AssetListView.as_view(), name='asset_list'),
    path('create/', views.AssetCreateView.as_view(), name='asset_create'),
    path('<int:pk>/', views.AssetDetailView.as_view(), name='asset_detail'),
    path('<int:pk>/edit/', views.AssetUpdateView.as_view(), name='asset_edit'),
    path('<int:pk>/delete/', views.AssetDeleteView.as_view(), name='asset_delete'),
]
