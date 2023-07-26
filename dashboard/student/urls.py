from django.urls import path

app_name = 'student_dashboard'

from . import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
    path('get/', views.GetStudent.as_view(), name='get_student'),
    path('add/', views.CreateStudent.as_view(), name='create_student'),
    path('detail/<int:pk>/', views.StudentDetail.as_view(), name='student_detail'),
    path('edit/<int:pk>/', views.UpdateStudent.as_view(), name='edit_student'),
    path('download/', views.DataView.as_view(), name='download_form'),
    path('download/data', views.DownloadDataView.as_view(), name='download_data'),
]
