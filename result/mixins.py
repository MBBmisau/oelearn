from django import dispatch
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from dashboard.result.utils import is_result_released
from custom_auth.models import CustomUser

class ResultReleasedReqiredMixin:

    def dispatch(self, request, *args, **kwargs):
        if not is_result_released(batch=self.batch):
            messages.error(request, 'Released result for selected batch is not found')
            if self.request.user.user_type == CustomUser.STUDENT:
                return redirect(reverse('student:dashboard'))
            return redirect(reverse('course_dashboard:dashboard'))
        return super().dispatch(request, *args, **kwargs)

class ResultReleaseForbiddenMixin:

    def dispatch(self, request, *args, **kwargs):
        if is_result_released(batch=self.batch):
            messages.error(request, 'Result is already released and hence unable to access requested url')
            if self.request.user.user_type == CustomUser.STUDENT:
                return redirect(reverse('student:dashboard'))
            return redirect(reverse('course_dashboard:dashboard'))
        return super().dispatch(request, *args, **kwargs)
    
