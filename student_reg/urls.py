from  django.urls import path

from . import views

app_name = 'student_reg'

urlpatterns = [
    path('', views.Register.as_view(), name='register'),
    path('validate_email', views.validate_email, name='validate_email'),
    path('success/', views.Success.as_view(), name='success'),
    path('activate/<uidb64>/<token>/', views.Activate.as_view(), name='activate'),
    path('invalidlink', views.InvalidActivationLink.as_view(), name='invalid_activation_link'),
    #path('profile/', views.profile, name='profile'),
    #path('profile/update/', views.profile_update, name='profile_update')
]
