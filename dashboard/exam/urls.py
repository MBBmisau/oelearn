from django.urls import path

app_name = 'exam_dashboard'

from . import views

urlpatterns = [
    #CA
    path('module/<int:module_id>/ca/<model_name>/create/', views.CreateUpdateCA.as_view(), name='add_ca'),
    path('module/<int:module_id>/ca/<model_name>/<id>/', views.CreateUpdateCA.as_view(), name='edit_ca'),
    path('module/<int:module_id>/ca/<model_name>/question/<paper_id>/', views.UpdateCAQuestion.as_view(), name='edit_ca_question'),
    path('ca/<int:pk>/delete', views.DeleteCA.as_view(), name='delete_ca'),
    #Exam
    path('course/<int:pk>', views.CourseExam.as_view(), name='course_exam'),
    path('course/<int:course_id>/exam/<model_name>/create/', views.CreateUpdateExam.as_view(), name='add_exam'),
    path('course/<int:course_id>/exam/<model_name>/<id>/', views.CreateUpdateExam.as_view(), name='edit_exam'),
    path('course/<int:course_id>/exam/<model_name>/question/<paper_id>/', views.UpdateExamQuestion.as_view(), name='edit_exam_question'),
    path('exam/<int:pk>/delete', views.DeleteExam.as_view(), name='delete_exam'),
    path('status/toggle/<course_id>/', views.ExamStatusToggle.as_view(), name='exam_status_toggle')
]