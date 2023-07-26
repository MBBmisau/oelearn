from django.urls import path
#from django.views.generic import TemplateView
from . import manage_views
from . import views

app_name = 'teacher'

urlpatterns = [
    #path('add/', manage_views.create_teacher, name='add_teacher'),
]
