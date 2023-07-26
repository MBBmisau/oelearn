from django.urls import path

app_name = 'result_dashboard'

from . import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
    path('release/', views.ReleaseResult.as_view(), name='release_result'),
    path('check/', views.CheckResult.as_view(), name='check_result'),
    path('student/<int:pk>/', views.StudentResultView.as_view(), name='student_result_view'),
    #Grade
    path('grade/add/', views.CreateGrade.as_view(), name='add_grade'),
    path('grade/<int:pk>/', views.UpdateGrade.as_view(), name='update_grade'),
    path('grade/<int:pk>/delete/', views.DeleteGrade.as_view(), name='delete_grade'),
    #CA
    path('module/<module_id>/ca/<ca_id>/result/', views.ModuleCAResult.as_view(), name='module_ca_result'),
    path('student/ca/mark/<int:pk>', views.MarkStudentCA.as_view(), name='mark_student_ca'),
    #Exam
    path('course/<course_id>/exam/<exam_id>/result/', views.CourseExamResult.as_view(), name='course_exam_result'),
    path('student/exam/mark/<int:pk>', views.MarkStudentExam.as_view(), name='mark_student_exam'),
]