from django.urls import path

app_name = 'course_dashboard'

from . import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
    #Subject
    path('subject/add/', views.CreateSubject.as_view(), name='add_subject'),
    path('subject/<int:pk>/', views.UpdateSubject.as_view(), name='edit_subject'),
    path('subject/<int:pk>/delete/', views.DeleteSubject.as_view(), name='delete_subject'),
    #Course
    path('add/', views.CreateCourse.as_view(), name='add_course'),
    path('<pk>/edit/', views.UpdateCourse.as_view(), name='edit_course'),
    path('<pk>/delete/', views.DeleteCourse.as_view(), name='delete_course'),
    path('add/<course_id>/student/', views.CouseAddStudent.as_view(), name='course_add_student'),
    # Module
    path('<pk>/module/', views.UpdateModule.as_view(), name='edit_module'),
    path('module/<int:module_id>/content/<model_name>/create/', views.CreateUpdateContent.as_view(),name='add_content'),
    path('module/<int:module_id>/content/<model_name>/<id>/', views.CreateUpdateContent.as_view(), name='edit_content'),
    path('content/<int:pk>/delete', views.DeleteContent.as_view(), name='delete_content'),
    path('module/<int:module_id>/', views.ModuleContentList.as_view(), name='content_list'),
    path('content/publish/toggle/<model_name>/<int:pk>/', views.PublishToggle.as_view(), name='publish_toggle'),
]
