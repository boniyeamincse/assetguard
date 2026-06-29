from django.urls import path
from . import views

app_name = 'teams'

urlpatterns = [
    path('', views.TeamListView.as_view(), name='team_list'),
    path('create/', views.TeamCreateView.as_view(), name='team_create'),
    path('<int:pk>/', views.TeamDetailView.as_view(), name='team_detail'),
    path('<int:pk>/edit/', views.TeamUpdateView.as_view(), name='team_edit'),
    path('<int:pk>/delete/', views.TeamDeleteView.as_view(), name='team_delete'),
    path('<int:team_id>/add-member/', views.add_team_member, name='add_member'),
    path('<int:team_id>/remove-member/<int:user_id>/', views.remove_team_member, name='remove_member'),
]
