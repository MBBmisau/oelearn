from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordContextMixin
from .models import CustomUser
from django.urls import reverse
from django.views.generic.base import TemplateView, RedirectView

from student.models import Student
from course.models import Course

class Home(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student_count'] = Student.objects.all().count()
        context['course_count'] = Course.objects.all().count()
        return context
    


@login_required
def account_redirect(request):
    user = request.user
    if user.user_type == CustomUser.STUDENT:
        return redirect(reverse('student:dashboard'))
    elif user.user_type == CustomUser.TEACHER:
        return redirect(reverse('dashboard:dashboard'))
    else:
        return redirect(reverse('dashboard:dashboard'))

class VerifyRedirect(RedirectView):
    #url = '/'
    def  get_redirect_url(self):
        return reverse('result:verify_result')