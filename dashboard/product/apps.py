from django.apps import AppConfig


class ProductDashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    label = 'product_dashboard'
    name = 'dashboard.product'
