from django.apps import AppConfig


class StudentDashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    label = 'student_dashboard'
    name = 'dashboard.student'
