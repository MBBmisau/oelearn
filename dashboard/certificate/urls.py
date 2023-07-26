from django.urls import path

app_name = 'certificate_dashboard'

from . import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
    path('add/', views.CreateCertificate.as_view(), name='create_certificate'),
    path('get', views.GetCertificate.as_view(), name='get_certificate'),
    path('<int:pk>/', views.UpdateCertificate.as_view(), name='update_certificate'),
    path('get/course/', views.GetCourseCertificate.as_view(), name='get_course_certificate'),
    path('batch/<batch_id>/course/<course_id>/', views.CourseCertificate.as_view(), name='course_certificate'),
]