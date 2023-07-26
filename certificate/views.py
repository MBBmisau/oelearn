from django.shortcuts import redirect, render
from django.urls import reverse
from certificate.models import Certificate
from result.forms import CheckResultForm
from django.contrib import messages
from result.models import StudentResult

from student.mixins import StudentTestMixin
from django.views.generic.base import TemplateView

class Index(StudentTestMixin, TemplateView):
    template_name = 'certificate/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.request.user.student
        context['certificates'] = Certificate.objects.filter(result__student=student)
        return context
    

class GetCertificate(StudentTestMixin, TemplateView):
    template_name = 'result/check_result.html'
    form = CheckResultForm

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST, user=self.request.user)
        if form.is_valid():
            student = self.request.user.student
            batch = form.cleaned_data.get('batch')
            course = form.cleaned_data.get('course')
            student_result = StudentResult.objects.get(student=student, course=course, batch=batch)
            try:
                certificate = Certificate.objects.get(result=student_result)
                messages.info(request, 'You already have certificate for this result')
                return redirect(reverse('certificate:index'))
            except Certificate.DoesNotExist:
                return redirect(reverse('payment:certificate_enrollment', kwargs={'result_id':student_result.id}))
        return self.render_to_response({'form':form,'meta_title':'Get | Certificate','title':'Get certificate','btn_text':'Proceed'})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form(user=self.request.user)
        context['meta_title'] = 'Get | Certificate'
        context['title'] = 'Get certificate'
        context['btn_text'] = 'Proceed'
        return context
