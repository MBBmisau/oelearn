from django.apps import AppConfig


class CustomAuthDashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    label = 'ccustom_auth_dashboard'
    name = 'dashboard.custom_auth'
