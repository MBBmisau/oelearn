from django.urls import path, include

app_name = 'dashboard'

from . import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
    path('profile', views.Profile.as_view(), name='profile'),
]
