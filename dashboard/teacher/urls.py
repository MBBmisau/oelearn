from django.urls import path

app_name = 'teacher_dashboard'

from . import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
    path('add/', views.CreateTeacher.as_view(), name='add_teacher'),
    path('detail/<int:pk>/', views.TeacherDetail.as_view(), name='teacher_detail'),
    path('edit/<int:pk>/', views.UpdateTeacher.as_view(), name='edit_teacher'),
]
