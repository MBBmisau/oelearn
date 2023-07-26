from django.urls import path

from . import views

app_name = 'custom_auth_dashboard'

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
    path('password_reset/', views.UserPasswordResetView.as_view(), name='user_password_reset'),
]