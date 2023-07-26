#from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordContextMixin
from django.views.generic.edit import FormView
#from django.conf import setti
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
#from django.contrib.auth import update_session_auth_hash
from django.views.generic.base import TemplateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
#from django.core.exceptions import ValidationError
from django.contrib import messages

from custom_auth.models import CustomUser
UserModel = get_user_model()

from .forms import UserPasswordResetForm

class Dashboard(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'admin'
    template_name = 'dashboard/custom_auth/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_count'] = UserModel.objects.all().count()
        return context

class UserPasswordResetView(LoginRequiredMixin, PermissionRequiredMixin, PasswordContextMixin, FormView):
    permission_required = 'admin'
    form_class = UserPasswordResetForm
    template_name = 'dashboard/custom_auth/user_password_reset.html'
    #success_url = reverse('custom_auth_dashboard:dashboard')
    title = 'Reset User Password'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_success_url(self):
        return reverse('custom_auth_dashboard:dashboard')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
       # kwargs['user'] = self.get_user()
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Password changed successfully!')
        return super().form_valid(form)
