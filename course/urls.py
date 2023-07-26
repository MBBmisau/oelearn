from django.urls import path

app_name = 'course'

from . import views

urlpatterns = [
    path('', views.EnrollIndex.as_view(), name='enroll_index'),
    path('register', views.NonrollIndex.as_view(), name='nonroll_index'),
    path('module/<int:module_id>', views.CourseDetail.as_view(), name='course_detail'),
]
