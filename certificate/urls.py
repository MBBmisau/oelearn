from django.urls import path

from . import views

app_name = 'certificate'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('get/', views.GetCertificate.as_view(), name='get_certificate'),
]
