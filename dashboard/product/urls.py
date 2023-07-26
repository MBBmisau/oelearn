from django.urls import path

app_name = 'product_dashboard'

from . import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
    path('add/', views.CreateProduct.as_view(), name='create_product'),
    path('<int:pk>/', views.UpdateProduct.as_view(), name='update_product'),
    path('delete/<int:pk>/', views.DeleteProduct.as_view(), name='delete_product'),
]