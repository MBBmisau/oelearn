from django.urls import path

app_name = 'product'

from . import views

urlpatterns = [
    path('user/', views.UserProductIndex.as_view(), name='user_product_index'),
    path('user/detail/<int:pk>/', views.UserProductDetail.as_view(), name='user_product_detail'),
    path('shop/', views.Shop.as_view(), name='shop'),
    path('<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
]