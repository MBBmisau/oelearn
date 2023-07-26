"""oelern URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve 

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url


urlpatterns = [
    path('', include('custom_auth.urls')),
    path('django-admin/', admin.site.urls),
    path('auth/', include("django.contrib.auth.urls")),
    path('course/', include('course.urls')),
    path('register/', include('student_reg.urls')),
    path('student/', include('student.urls')),
    path('payment/', include('payment.urls')),
    path('academic/', include('academic.urls')),
    path("paystack/", include(('paystack.urls', 'paystack'),namespace='paystack')),
    path('exam/', include('exam.urls')),
    path('product/', include('product.urls')),
    path('result/', include('result.urls')),
    path('certificate/', include('certificate.urls')),

    path('dashboard/', include('dashboard.urls')),
    path('dashboard/teacher/', include('dashboard.teacher.urls')),
    path('dashboard/course/', include('dashboard.course.urls')),
    path('dashboard/product/', include('dashboard.product.urls')),
    path('dashboard/account/', include('dashboard.custom_auth.urls')),
    path('dashboard/result/', include('dashboard.result.urls')),
    path('dashboard/exam/', include('dashboard.exam.urls')),
    path('dashboard/certificate/', include('dashboard.certificate.urls')),
    path('dashboard/academic/', include('dashboard.academic.urls')),
    path('dashboard/student/', include('dashboard.student.urls')),
    
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
