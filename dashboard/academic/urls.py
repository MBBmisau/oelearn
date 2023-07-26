from django.urls import path

app_name = 'academic_dashboard'

from . import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
    #Batch
    path('batch/graduate/', views.GraduateBatch.as_view(), name='graduate_batch'),
    path('batch/status/toggle/', views.BatchStatusToggle.as_view(), name='batch_status_toggle'),
    path('batch/add/', views.CreateBatch.as_view(), name='create_batch'),
    path('batch/<int:pk>/', views.UpdateBatch.as_view(), name='update_batch'),
    path('batch/<int:pk>/delete/', views.DeleteBatch.as_view(), name='delete_batch'),
]