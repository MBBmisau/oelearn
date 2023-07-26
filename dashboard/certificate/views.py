from unittest import result
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic.base import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from academic.models import Batch
from certificate.models import Certificate
from course.models import Course
from .forms import GetCourseCertificateForm
from django_tables2 import SingleTableView
from django.views.generic.edit import UpdateView

from dashboard.result.forms import CheckResultForm
from .tables import CourseCerficateTable
from student.models import Student
from result.models import StudentResult

class Dashboard(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'admin'
    template_name = 'dashboard/certificate/dashboard.html'
    
class CreateCertificate(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'admin'
    template_name = 'dashboard/certificate/form.html'
    form = CheckResultForm

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            student = Student.objects.get(user__email__exact=email)
            batch = form.cleaned_data.get('batch')
            course = form.cleaned_data.get('course')
            student_result = StudentResult.objects.get(student=student, course=course, batch=batch)
            certificate = Certificate.objects.get_or_create(result=student_result)[0]
            return redirect(reverse('certificate_dashboard:update_certificate', kwargs={'pk': certificate.pk}))
        return self.render_to_response({'form': form, 'meta_title':'Create | Certificate','title':'Create certificate','btn_text':'Create'})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form()
        context['meta_title'] = 'Create | Certificate'
        context['title'] = 'Create certificate'
        context['btn_text'] = 'Create'
        return context
    

class GetCertificate(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'admin'
    form = CheckResultForm
    template_name = 'dashboard/certificate/form.html'

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            student = Student.objects.get(user__email__exact=email)
            batch = form.cleaned_data.get('batch')
            course = form.cleaned_data.get('course')
            student_result = StudentResult.objects.get(student=student, course=course, batch=batch)
            try:
                certificate = Certificate.objects.get(result=student_result)
                return redirect(reverse('certificate_dashboard:update_certificate', kwargs={'pk': student_result.certificate.pk}))
            except Certificate.DoesNotExist:
                messages.error(request, 'Unable to find certificate, Please! Add certificate to that result first.')
                return redirect(reverse('certificate_dashboard:dashboard'))
        return self.render_to_response({'form': form,'meta_title':'Get | Certificate','title': 'Get Certificate','btn_text': 'Get Certificate'})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form()
        context['meta_title'] = 'Get | Certificate'
        context['title'] = 'Get Certificate'
        context['btn_text'] = 'Get certificate'
        return context        

class UpdateCertificate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'admin'
    model = Certificate
    fields = ['file']
    template_name = 'dashboard/certificate/update_certificate.html'
    
    def get_success_url(self):
        course = self.object.result.course
        batch = self.object.result.batch
        return reverse('certificate_dashboard:course_certificate', kwargs={'course_id': course.id,'batch_id':batch.id})

class GetCourseCertificate(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'admin'
    form = GetCourseCertificateForm
    template_name = 'dashboard/certificate/form.html'

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            batch = form.cleaned_data.get('batch')
            course = form.cleaned_data.get('course')
            return redirect(reverse('certificate_dashboard:course_certificate', kwargs={'batch_id':batch.id,'course_id':course.id}))
        return self.render_to_response({'form':form, 'title': 'Get course certificates','btn_text': 'Get certificates',})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form()
        context['meta_title'] = 'Get | Course Cerficate'
        context['title'] = 'Get course certificates'
        context['btn_text'] = 'Get certificates'
        return context
    

class CourseCertificate(LoginRequiredMixin, PermissionRequiredMixin, SingleTableView):
    permission_required = 'admin'
    template_name = 'dashboard/certificate/course_certificate.html'
    table_class = CourseCerficateTable

    def dispatch(self, request, batch_id, course_id, *args, **kwargs):
        self.batch = get_object_or_404(Batch, id=batch_id)
        self.course = get_object_or_404(Course, id=course_id)
        return super().dispatch(request, batch_id, course_id, *args, **kwargs)
    
    def get_queryset(self):
        return Certificate.objects.filter(result__batch=self.batch,result__course=self.course)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.course
        context['batch'] = self.batch
        return context
    