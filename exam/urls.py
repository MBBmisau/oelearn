from django.urls import path

app_name = 'exam'

from . import views

urlpatterns = [
    path('ca/<ca_id>/take/module/<module_id>/paper/<paper_model>/<int:pk>', views.TakeCA.as_view(), name='take_ca'),
    path('<exam_id>/take/course/<course_id>/paper/<paper_model>/<int:pk>/', views.TakeExam.as_view(), name='take_exam'),
    path('course/<course_id>/', views.CourseExamIndex.as_view(), name='course_exam_index'),
]
