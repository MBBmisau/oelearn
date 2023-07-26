from django import dispatch
from django.views.generic.base import View, TemplateResponseMixin
from django.forms.models import modelform_factory
from django.apps import apps
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import DeleteView
from django.views.generic.detail import DetailView
from dashboard import course
from django.views.generic.base import TemplateView

from dashboard.exam.forms import ObjectiveFormSet, EssayFormSet, AssignmentFormSet, ObjectiveForm, EssayForm, AssignmentForm
from exam.models import CA, Exam, Objective, ObjectiveQuestion, Essay, EssayQuestion, Assignment, AssignmentQuestion   
from dashboard.mixins import AdminOrInstructorMixin, AdminOrTeacherMixin
from course.models import Course, Module
from django.contrib import messages

class CreateUpdateCA(AdminOrInstructorMixin, TemplateResponseMixin, View):
    module = None
    model = None
    obj = None

    template_name = 'general/general_form.html'
    #template_name = "dashboard/course/content_form..html"

    def get_model(self, model_name):
        if model_name in ['objective', 'essay', 'assignment']:
            return apps.get_model(app_label='exam', model_name=model_name)
        return None

    def get_ca_form(self, model, model_name, *args, **kwargs):
        if model_name == 'objective':
            Form = ObjectiveForm
        if model_name == 'essay':
            Form = EssayForm
        if model_name == 'assignment':
            Form = AssignmentForm
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module, id=module_id)
        self.course = self.module.course
        self.model = self.get_model(model_name)
        self.parent_url = reverse('course_dashboard:content_list', kwargs={'module_id':self.module.id})
        if id:
            self.obj = get_object_or_404(self.model, id=id)

        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_ca_form(self.model, model_name, instance=self.obj)
        return self.render_to_response({'form': form, 'object': self.obj, 'title': f'Assessment | {model_name}', 'parent_url':self.parent_url})

    def post(self, request, module_id, model_name, id=None):
        form = self.get_ca_form(self.model, model_name, instance=self.obj, data=request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            if not id:
                CA.objects.create(module=self.module, paper=obj)

            return redirect(reverse('course_dashboard:content_list', kwargs={'module_id': self.module.id}))

        return self.render_to_response({'form': form, 'object': self.obj, 'parent_url': self.parent_url})

class UpdateCAQuestion(AdminOrInstructorMixin, TemplateResponseMixin, View):
    #template_name = 'general/general_form.html' 
    template_name = 'dashboard/exam/ca_question_form.html'
    course = None
    paper = None
    module = None
    model = None

    def get_model(self, model_name):
        if model_name in ['objective', 'essay', 'assignment']:
            return apps.get_model(app_label='exam', model_name=model_name)
        return None

    def get_formset(self, model_name, data=None):
        if self.model_name == 'objective':
            return ObjectiveFormSet(instance=self.paper, data=data)
        elif self.model_name == 'essay':
            return EssayFormSet(instance=self.paper, data=data)
        elif self.model_name == 'assignment':
            return AssignmentFormSet(instance=self.paper, data=data)


    def dispatch(self, request, module_id, model_name, paper_id, *args, **kwargs):
        self.module = get_object_or_404(Module, id=module_id)
        self.course = self.module.course
        self.model = self.get_model(model_name)
        self.paper = get_object_or_404(self.model, id=paper_id)
        self.model_name = model_name
        self.parent_url = reverse('course_dashboard:content_list', kwargs={'module_id':self.module.id})
        return super().dispatch(request, module_id, model_name, paper_id, *args, **kwargs)

    def get(self, request, model_name, *args, **kwargs):
        formset = self.get_formset(model_name)
        return self.render_to_response({'module': self.module, 'info':f'CA: {self.module}', 'total_marks':self.paper.total_marks, 'course':self.course, 'paper': self.model_name, 'formset': formset, 'parent_url': self.parent_url})

    def post(self, request, model_name, *args, **kwargs):
        formset = self.get_formset(model_name, data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect(reverse('course_dashboard:content_list', kwargs={'module_id': self.module.id}))
        return self.render_to_response({'module': self.module, 'total_marks':self.paper.total_marks, 'course':self.course, 'paper': self.model_name, 'formset': formset, 'parent_url': self.parent_url})

class DeleteCA(AdminOrInstructorMixin, SuccessMessageMixin, DeleteView):
    model = CA
    template_name = 'general/general_confirm_delete.html'
    success_url = reverse_lazy('course_dashboard:dashboard')
    success_message = 'CA ({}) deleted successfully'

    def dispatch(self, request, pk):
        self.ca = get_object_or_404(CA, pk=pk)
        self.module = self.ca.module
        self.course = self.module.course
        return super().dispatch(request, pk)

    def post(self, request, *args, **kwargs):
        self.ca.paper.delete()
        self.ca.delete()

        return redirect(reverse('course_dashboard:content_list', kwargs={'module_id': self.module.id})) #super().post(kwargs)

    def get_success_url(self):
        return redirect(reverse('course_dashboard:content_list', kwargs={'module_id': self.module.id}))

####---Exam----###
class CourseExam(AdminOrInstructorMixin, TemplateView):
    template_name = 'dashboard/exam/course_exam.html'
    context_object_name = course
    model = Course

    def dispatch(self, request, pk, *args, **kwargs):
        self.object = get_object_or_404(Course, pk=pk)
        return super().dispatch(request, *args, **kwargs)
    

    def get_exams(self):
        return Exam.objects.filter(course=self.object)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.object
        context['exams'] = self.get_exams()
        context['exams_count'] = self.get_exams().count()
        context['live_exam_count'] = self.get_exams().filter(live=True).count()
        return context
    

class CreateUpdateExam(AdminOrInstructorMixin, TemplateResponseMixin, View):
    course = None
    model = None
    obj = None

    template_name = 'general/general_form.html'
    #template_name = "dashboard/course/content_form..html"

    def get_model(self, model_name):
        if model_name in ['objective', 'essay']:
            return apps.get_model(app_label='exam', model_name=model_name)
        return None

    def get_form(self, model, model_name, *args, **kwargs):
        if model_name == 'objective':
            Form = ObjectiveForm
        if model_name == 'essay':
            Form = EssayForm
        return Form(*args, **kwargs)

    def dispatch(self, request, course_id, model_name, id=None):
        self.course = get_object_or_404(Course, id=course_id)
        self.model = self.get_model(model_name)
        self.parent_url = reverse('exam_dashboard:course_exam', kwargs={'pk':self.course.pk})
        if id:
            self.obj = get_object_or_404(self.model, id=id)

        return super().dispatch(request, course_id, model_name, id)

    def get(self, request, course_id, model_name, id=None):
        form = self.get_form(self.model, model_name, instance=self.obj)
        return self.render_to_response({'form': form, 'object': self.obj, 'title': f'Exam | {model_name}', 'parent_url':self.parent_url})

    def post(self, request, course_id, model_name, id=None):
        form = self.get_form(self.model, model_name, instance=self.obj, data=request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            if not id:
                Exam.objects.create(course=self.course, paper=obj)

            return redirect(self.parent_url)

        return self.render_to_response({'form': form, 'object': self.obj, 'parent_url': self.parent_url})

class UpdateExamQuestion(AdminOrInstructorMixin, TemplateResponseMixin, View):
    #template_name = 'general/general_form.html' 
    template_name = 'dashboard/exam/ca_question_form.html'
    course = None
    paper = None
    module = None
    model = None

    def get_model(self, model_name):
        if model_name in ['objective', 'essay']:
            return apps.get_model(app_label='exam', model_name=model_name)
        return None

    def get_formset(self, model_name, data=None):
        if self.model_name == 'objective':
            return ObjectiveFormSet(instance=self.paper, data=data)
        elif self.model_name == 'essay':
            return EssayFormSet(instance=self.paper, data=data)

    def dispatch(self, request, course_id, model_name, paper_id, *args, **kwargs):
        self.course = get_object_or_404(Course, id=course_id)
        self.model = self.get_model(model_name)
        self.paper = get_object_or_404(self.model, id=paper_id)
        self.model_name = model_name
        self.parent_url = reverse('exam_dashboard:course_exam', kwargs={'pk':self.course.pk})
        return super().dispatch(request, course_id, model_name, paper_id, *args, **kwargs)

    def get(self, request, model_name, *args, **kwargs):
        formset = self.get_formset(model_name)
        return self.render_to_response({'total_marks':self.paper.total_marks, 'info': f'Exam: {self.paper}', 'course':self.course, 'paper': self.model_name, 'formset': formset, 'parent_url': self.parent_url})

    def post(self, request, model_name, *args, **kwargs):
        formset = self.get_formset(model_name, data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect(self.parent_url)
        return self.render_to_response({'total_marks':self.paper.total_marks, 'course':self.course, 'paper': self.model_name, 'formset': formset, 'parent_url': self.parent_url})

class DeleteExam(AdminOrInstructorMixin, SuccessMessageMixin, DeleteView):
    model = Exam
    template_name = 'general/general_confirm_delete.html'
    success_message = 'Exam ({}) deleted successfully'

    def dispatch(self, request, pk):
        self.exam = get_object_or_404(Exam, pk=pk)
        self.course = self.exam.course
        self.parent_url = reverse('exam_dashboard:course_exam', kwargs={'pk':self.course.pk})
        return super().dispatch(request, pk)

    def post(self, request, *args, **kwargs):
        self.exam.paper.delete()
        self.exam.delete()

        return redirect(self.parent_url)

    def get_success_url(self):
        return redirect(self.parent_url)

class ExamStatusToggle(AdminOrInstructorMixin, View):

    def dispatch(self, request, course_id, *args, **kwargs):
        self.course = get_object_or_404(Course, id=course_id)
        self.redirect_to = reverse('exam_dashboard:course_exam', kwargs={'pk':self.course.pk})
        return super().dispatch(request, course_id, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.course.exam_open:
            self.course.exam_open = False
            self.course.save()
            messages.info(request, 'Exam successfully closed')
            return redirect(self.redirect_to)
        self.course.exam_open = True
        self.course.save()
        messages.success(request, 'Exam successfully Opened')
        return redirect(self.redirect_to)
    
