from django.urls import path

from . import views

app_name = 'academic'

urlpatterns = [
    path('closed', views.PortalClosed.as_view(), name='portal_closed'),
    ]
