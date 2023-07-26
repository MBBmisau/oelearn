from django.views.generic.detail import DetailView
from django.forms.models import modelform_factory
from django.apps import apps
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import View, TemplateResponseMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_tables2.views import SingleTableView
from django.contrib.messages.views import SuccessMessageMixin
from bootstrap_datepicker_plus.widgets import TimePickerInput
from django.contrib import messages

from dashboard.mixins import AdminOrInstructorMixin, AdminOrTeacherMixin
from course.models import Course, Module, Content, Subject, Video
from exam.models import Exam
from .forms import ModuleFormSet
from student.models import Student
from .utils import has_live_video

from .tables import SubjectTable


class Dashboard(AdminOrTeacherMixin, SingleTableView):
    table_class = SubjectTable
    model = Subject
    template_name = 'dashboard/course/dashboard.html'

    def get_courses(self):
        if self.request.user.is_admin:
            return Course.objects.all()
        return Course.objects.filter(instructor=self.request.user.teacher)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = self.get_courses()
        return context

class CreateSubject(LoginRequiredMixin, SuccessMessageMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'admin'
    model = Subject
    fields = '__all__'
    template_name = 'general/general_form.html'
    success_message = 'Subject was added successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add new subject'
        return context

class UpdateSubject(LoginRequiredMixin, SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'admin'
    model = Subject
    fields = '__all__'
    template_name = 'general/general_form.html'
    success_message = 'Subject was updated successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit subject'
        return context

class DeleteSubject(LoginRequiredMixin, SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'admin'
    model = Subject
    template_name = 'general/general_confirm_delete.html'
    success_url = reverse_lazy('course_dashboard:dashboard')
    success_message = 'Subject ({}) deleted successfully'

class CreateCourse(LoginRequiredMixin, SuccessMessageMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'admin'
    model = Course
    fields = ['title', 'instructor', 'subject', 'overview', 'price', 'is_free', 'certificate_price', 'is_certificate_free', 'registration_open', 'live']
    template_name = 'general/general_form.html'
    success_message = 'Course was added successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add New Course'
        return context


class UpdateCourse(LoginRequiredMixin, SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'admin'
    model = Course
    fields = ['title', 'instructor', 'subject', 'overview', 'price', 'is_free', 'certificate_price', 'is_certificate_free', 'registration_open', 'live']
    template_name = 'general/general_form.html'
    success_message = 'Course was edited successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit subject'
        return context


class DeleteCourse(LoginRequiredMixin, SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'admin'
    model = Course
    template_name = 'general/general_confirm_delete.html'
    success_url = reverse_lazy('course_dashboard:dashboard')
    success_message = 'Course ({}) deleted successfully'

class CouseAddStudent(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'admin'

    def dispatch(self, request, course_id):
        self.course = get_object_or_404(Course, id=course_id)

        return super().dispatch(request, course_id)

    def get(self, request, course_id):
        email = request.GET.get('student-email')
        try:
            student = Student.objects.get(user__email=email)
        except Exception as e:
            student = None
        if student:
            self.course.students.add(student)
            messages.success(request, f'{student.user} added to {self.course} successfully')
            return redirect(reverse('course_dashboard:dashboard'))
        messages.error(request, f'Student with email ({email}), is found')
        return redirect(reverse('course_dashboard:dashboard'))

# ---------------Modula View----------------
class UpdateModule(AdminOrInstructorMixin, TemplateResponseMixin, View):
    template_name = 'dashboard/course/module_form.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, pk=pk)

        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect(reverse("course_dashboard:dashboard"))
        return self.render_to_response({'course': self.course, 'formset': formset})


class ModuleContentList(AdminOrInstructorMixin, TemplateResponseMixin, View):
    template_name = 'dashboard/course/content_list.html'

    def dispatch(self, request, module_id):
        self.module = get_object_or_404(Module, id=module_id)
        self.course = self.module.course
        return super().dispatch(request, module_id)

    def get(self, request, module_id):
        module = self.module
        course = self.course
        return self.render_to_response({"module": module, 'course': course})

class PublishToggle(AdminOrInstructorMixin, View):

    def get_model(self, model_name):
        if model_name == 'content':
            return apps.get_model(app_label='course', model_name=model_name)
        elif model_name == 'ca':
            return apps.get_model(app_label='exam', model_name=model_name)
        elif model_name == 'exam':
            return apps.get_model(app_label='exam', model_name=model_name)
        return None

    def dispatch(self, request, model_name, pk):
        self.model = self.get_model(model_name)
        self.obj = get_object_or_404(self.model, pk=pk)
        return super().dispatch(request, model_name, pk)
    
    def get_redirect_to(self):
        if type(self.obj) == Exam:
            return reverse('exam_dashboard:course_exam', kwargs={'pk':self.obj.course.pk})
        return reverse('course_dashboard:content_list', kwargs={'module_id': self.obj.module.id})
    
    def get(self, request, model_name, *args, **kwargs):
        redirect_to = self.get_redirect_to()
        if model_name == 'ca' or model_name == 'exam':
            ce_marks = self.obj.paper.total_marks
            ce_question_marks = 0
            for ce_q in self.obj.paper.questions.all():
                ce_question_marks += ce_q.marks
            if not self.obj.live and ce_marks != ce_question_marks:
                messages.error(request, f'Unable to publish "{model_name.upper()}", total marks is not equal to the sum of marks of questions.')
                return redirect(redirect_to)
        if model_name == 'content':
            if type(self.obj.item) == Video:
                if has_live_video(self.obj.module) and not self.obj.live:
                    messages.error(request, 'Module must not have morethan one video published.')
                    return redirect(redirect_to)
        if self.obj.live:
            self.obj.live = False
            self.obj.save()
            messages.info(request, f'"{self.obj}" Unpublished successfully.')
            return redirect(redirect_to)
        self.obj.live = True
        self.obj.save()
        messages.success(request, f'"{self.obj}" Published successfully.')
        return redirect(redirect_to)

# ----------------Content Views----------------
class CreateUpdateContent(AdminOrInstructorMixin, TemplateResponseMixin, View):
    module = None
    model = None
    obj = None

    template_name = 'general/general_form.html'
    #template_name = "dashboard/course/content_form.html"

    def get_model(self, model_name):
        if model_name in ['text', 'image', 'video', 'file']:
            return apps.get_model(app_label='course', model_name=model_name)
        return None

    def get_form(self, model, model_name, *args, **kwargs):
        if model_name == 'file':
            Form = modelform_factory(model, exclude=['size', 'format', 'created', 'updated'])
        else:
            Form = modelform_factory(model, exclude=['created', 'updated'])

        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module, id=module_id)
        self.course = get_object_or_404(Course, id=self.module.course.id)
        self.model = self.get_model(model_name)
        self.parent_url = reverse('course_dashboard:content_list', kwargs={'module_id':self.module.id})
        if id:
            self.obj = get_object_or_404(self.model, id=id)

        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, model_name, instance=self.obj)
        return self.render_to_response({'form': form, 'object': self.obj, 'title': 'Content', 'parent_url': self.parent_url})

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, model_name, instance=self.obj, data=request.POST, files=request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            if not id:
                Content.objects.create(module=self.module, item=obj)

            return redirect(reverse('course_dashboard:content_list', kwargs={'module_id': self.module.id}))

        return self.render_to_response({'form': form, 'object': self.obj, 'parent_url': self.parent_url})

class DeleteContent(AdminOrInstructorMixin, SuccessMessageMixin, DeleteView):
    model = Content
    template_name = 'general/general_confirm_delete.html'
    success_url = reverse_lazy('course_dashboard:dashboard')
    success_message = 'Content ({}) deleted successfully'

    def dispatch(self, request, pk):
        self.content = get_object_or_404(Content, pk=pk)
        self.module = self.content.module
        self.course = self.module.course
        return super().dispatch(request, pk)

    def post(self, request, *args, **kwargs):
       self.content.item.delete()
       self.content.delete()

       return redirect(reverse('course_dashboard:content_list', kwargs={'module_id': self.module.id})) #super().post(request, *args, **kwargs)

    def get_success_url(self):
        return redirect(reverse('course_dashboard:content_list', kwargs={'module_id': self.module.id}))