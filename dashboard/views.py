from  django.views.generic.base import TemplateView, View
from django.contrib.auth.mixins import PermissionRequiredMixin

from .mixins import AdminOrTeacherMixin

class Dashboard(AdminOrTeacherMixin, TemplateView):
    template_name =  'dashboard/dashboard.html'

class Profile(AdminOrTeacherMixin, TemplateView):
    template_name =  'dashboard/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.request.user.teacher
        return context
    
