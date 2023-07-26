from django.urls import path

from . import views

app_name = 'config'

urlpatterns = [
    path('', views.ConfigView.as_view(), name='config'),
    path('save/', views.SaveSettings.as_view(), name='save_school_settings'),

    path('address/save/', views.SaveAddress.as_view(), name='save_school_address'),

    path('social/create/', views.CreateSocialLink.as_view(), name='create_social_link'),
    path('social/<int:pk>/', views.UpdateSocialLink.as_view(), name='update_social_link'),
    path('<int:pk>/delete/', views.DeleteSocialLink.as_view(), name='delete_social_link'),
]
