from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
    #path('registration/<int:pk>/', views.Registration.as_view(), name='registration'),
    path('enroll/course/<int:course_id>/', views.CourseEnrollment.as_view(), name='course_enrollment'),
    path('certificate/<int:result_id>/', views.CertificateEnrollment.as_view(), name='certificate_enrollment'),
    path('product/<int:pk>/', views.BuyProduct.as_view(), name='buy_product'),
]
