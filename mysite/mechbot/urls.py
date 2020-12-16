from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('alerts', views.mechbot_alerts, name='mechbot_alerts'),
    path('docs', views.mechbot_docs, name='mechbot_docs'),
    path('new_alert/', views.new_alert, name='new_alert'),
    path('discord/', views.discord_server_redirect, name='discord_server_redirect'),
    path('update_alert/<str:pk>/', views.update_alert, name='update_alert'),
    path('delete_alert/<str:pk>/', views.delete_alert, name='delete_alert'),
    path('oauth2/login', views.discord_login, name='oauth2_login'),
    path('oauth2/login/redirect', views.discord_login_redirect, name='discord_login_redirect'),
]