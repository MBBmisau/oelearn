from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from course.models import Course
from .tables import BatchTable
from django_tables2 import SingleTableView
from django.views.generic.base import TemplateView, View

from academic.models import Batch
from dashboard.result.utils import BATCH, is_result_released

class Dashboard(LoginRequiredMixin, PermissionRequiredMixin, SingleTableView):
    permission_required = 'admin'
    template_name = 'dashboard/academic/dashboard.html'
    table_class = BatchTable
    model = Batch

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            batch = Batch.objects.get(is_current=True)
        except Batch.DoesNotExist: 
            batch = None
        context['current_batch'] = batch
        return context

class GraduateBatch(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'admin'
    template_name = 'dashboard/academic/graduate_batch.html'

    def dispatch(self, request, *args, **kwargs):
        redirect_to = reverse('academic_dashboard:dashboard')
        if not is_result_released(BATCH):
            messages.info(request, 'Result must be released for batch to be graduated.')
            return redirect(redirect_to)
        self.current_batch = Batch.objects.get(is_current=True)
        if not self.current_batch.next_batch:
            messages.info(request, 'Current batch must have next batch. Please! set next batch manually')
            return redirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        next_batch = self.current_batch.next_batch
        courses = Course.objects.all()
        for course in courses:
            course.students.clear()
        next_batch.is_current = True
        next_batch.save()
        Batch.objects.exclude(id=next_batch.id).update(is_current=False)
        return redirect(reverse('academic_dashboard:dashboard'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_batch'] = self.current_batch
        context['next_batch'] = self.current_batch.next_batch
        return context

class BatchStatusToggle(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'admin'

    def dispatch(self, request, *args, **kwargs):
        self.batch = Batch.objects.get(is_current=True)
        self.redirect_to = reverse('academic_dashboard:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.batch.live:
            self.batch.live = False
            self.batch.save()
            messages.info(request, 'Batch successfully closed')
            return redirect(self.redirect_to)
        self.batch.live = True
        self.batch.save()
        messages.success(request, 'Batch successfully Opened')
        return redirect(self.redirect_to)

class CreateBatch(LoginRequiredMixin, SuccessMessageMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'admin'
    model = Batch
    fields = ['name', 'order', 'next_batch', 'description']
    template_name = 'general/general_form.html'
    success_message = 'Batch was added successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add new batch'
        return context

class UpdateBatch(LoginRequiredMixin, SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'admin'
    model = Batch
    fields = ['name', 'order', 'next_batch', 'description']
    template_name = 'general/general_form.html'
    success_message = 'Batch was updated successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit batch'
        return context

class DeleteBatch(LoginRequiredMixin, SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'admin'
    model = Batch
    template_name = 'general/general_confirm_delete.html'
    success_url = reverse_lazy('academic_dashboard:dashboard')
    success_message = 'Batch ({}) deleted successfully'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_current:
            messages.error(request, 'Current session can not be deleted')
            return redirect(reverse('academic_dashboard:dashboard'))
        return super().post(request, *args, **kwargs)