from  django.views.generic.base import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

from .mixins import StudentTestMixin

class Dashboard(StudentTestMixin, TemplateView):
    template_name = 'student/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.request.user.student
        context['student'] = student
        context['courses_enrolled_count'] = student.courses_joined.all().count()
        context['my_product_count'] = student.user.product_set.all().count()
        return context

class AccessDenied(TemplateView):
    template_name = 'student/access_denied.html'

class Profile(StudentTestMixin, TemplateView):
    template_name =  'student/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.request.user.student
        return context