from django.urls import path, reverse
from django.views.generic.base import RedirectView

from . import views

app_name = 'custom_auth'

urlpatterns = [
    #path('', views.Home.as_view(), name='home'),
    path('', views.account_redirect, name='home'),
    path('redirect/', views.account_redirect, name='account_redirect'),
    path('verify/', views.VerifyRedirect.as_view(), name='verify_redirect'),
]