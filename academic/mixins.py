from pyexpat.errors import messages
from django.contrib import messages as django_messages
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.mixins import UserPassesTestMixin
from requests import request

from student.models import Student
 
from . import utils

class CurrentBatchRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        self.batch = utils.get_current_batch()
        if utils.get_current_batch() is None:
            return redirect(reverse('academic:portal_closed'))
        return super().dispatch(request, *args, **kwargs)

class CurrentBatchLiveMixin:
    #To be inherited by course enrollment, enroll index, Exam, CA, etc
    #There must have current batch and current batch must be live
    def dispatch(self, request, *args, **kwargs):
        self.batch = utils.get_current_batch()
        redirect_to = reverse('student:dashboard')
        if self.batch is None:
            django_messages.error(request, 'Batch must be set for student to access this url')
            return redirect(redirect_to)
        if not self.batch.live:
            django_messages.info(request, 'Current batch is temporarily closed')
            return redirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)