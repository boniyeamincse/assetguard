from django.urls import path
from . import views

app_name = 'settings'

urlpatterns = [
    path('', views.settings_index, name='settings_index'),
    path('general/', views.general_settings, name='general_settings'),
    path('server-monitor/', views.server_monitor, name='server_monitor'),
    path('notifications/', views.notification_settings, name='notification_settings'),
    path('security/', views.security_settings, name='security_settings'),
]
