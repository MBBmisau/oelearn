from django.urls import path
#from django.views.generic import TemplateView
#from . import manage_views
from . import views

app_name = 'student'

urlpatterns = [
    path('accessdenied', views.AccessDenied.as_view(), name='access_denied'),
    #path('add/', manage_views.create_student, name='add_student'),
    #path('manage/', manage_views.ManageStudent.as_view(), name='manage'),
    #path('add/success/<int:pk>/', manage_views.AddStudentSuccess.as_view(), name ='success'),
    #path('add/admission/<int:pk>/', manage_views.StudentAdmissionLetter.as_view(), name ='admission'),
    #path('detail/<int:pk>/', manage_views.StudentDetail.as_view(), name ='student_detail'),
    #path('update/<int:pk>/', manage_views.update_student, name ='update_student'),
    #path('graduate/', manage_views.Graduate.as_view(), name ='graduate'),
    #path('graduate_student/', manage_views.GraduateStudent.as_view(), name ='graduate_student'),
    #path('suspension/', manage_views.Suspension.as_view(), name ='suspension'),
    #path('suspend_student/', manage_views.SuspendStudent.as_view(), name ='suspend_student'),

    path('', views.Dashboard.as_view(), name='dashboard'),
    path('profile/', views.Profile.as_view(), name='profile'),
    #path('timetable/', views.StudentTimetable.as_view(), name ='timetable'),
    #path('timetable/download/', views.StudentTimetableDownload.as_view(), name ='timetable_download'),
]
