from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django_tables2 import MultiTableMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import TemplateView

from .forms import CheckResultForm, VerifyResultForm
from .tables import StudentCATable, StudentExamTable
from .models import StudentResult
from student.mixins import StudentTestMixin
from student.models import Student

class CheckResult(StudentTestMixin, TemplateView):
    form = CheckResultForm
    template_name = 'result/check_result.html'

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST, user=self.request.user)
        if form.is_valid():
            student = self.request.user.student
            batch = form.cleaned_data.get('batch')
            course = form.cleaned_data.get('course')
            student_result = StudentResult.objects.get(student=student, course=course, batch=batch)
            return redirect(reverse('result:student_result_view', kwargs={'pk':student_result.pk}))
        return self.render_to_response({'form':form,'meta_title':'Check | Result','title':'Check my result','btn_text':'Check result'})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form(user=self.request.user)
        context['meta_title'] = 'Check | Result'
        context['title'] = 'Check my result'
        context['btn_text'] = 'Check result'
        return context
    

class StudentResultView(StudentTestMixin, MultiTableMixin, TemplateView):
    template_name = 'result/student_result_view.html'
       
    def dispatch(self, request, pk, *args, **kwargs):
        self.result = get_object_or_404(StudentResult, pk=pk)
        return super().dispatch(request, *args, **kwargs)
    
    def get_tables(self):
        return [
            StudentCATable(self.result.cas.all()),
            StudentExamTable(self.result.exams.all()),
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['result'] = self.result
        context['parent_url'] = reverse('result:check_result')
        return context

class VerifyResult(TemplateView):
    form = VerifyResultForm
    template_name = 'result/verify_result.html'

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            reg_id = form.cleaned_data.get('reg_id')
            batch = form.cleaned_data.get('batch')
            course = form.cleaned_data.get('course')
            student = Student.objects.get(user__reg_id__exact=reg_id)
            student_result = StudentResult.objects.get(student=student, course=course, batch=batch)
            return redirect(reverse('result:verify_result_view', kwargs={'pk':student_result.pk,}))
        return self.render_to_response({'form':form,'meta_title':'Verify | Result','title':'Verify student result','btn_text':'Verify result'})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form()
        context['meta_title'] = 'Verify | Result'
        context['title'] = 'Verify student result'
        context['btn_text'] = 'Verify result'
        return context

class VerifyResultView(TemplateView):
    template_name = 'result/verify_result_view.html'
       
    def dispatch(self, request, pk, *args, **kwargs):
        self.result = get_object_or_404(StudentResult, pk=pk)
        return super().dispatch(request, pk, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['result'] = self.result
        context['object'] = self.result.student #used in verify view
        context['parent_url'] = reverse('result:verify_result')
        return context