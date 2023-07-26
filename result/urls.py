from django.urls import path

app_name = 'result'

from . import views

urlpatterns = [
    path('check/', views.CheckResult.as_view(), name='check_result'),
    path('student/<int:pk>/', views.StudentResultView.as_view(), name='student_result_view'),
    path('verify/', views.VerifyResult.as_view(), name='verify_result'),
    path('verify/student/<int:pk>/', views.VerifyResultView.as_view(), name='verify_result_view'),
]