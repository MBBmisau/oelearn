from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from academic.utils import get_current_batch
from django.views.generic.base import TemplateView, View
from django.contrib import messages
from dashboard import exam, result
from django_tables2 import SingleTableView, MultiTableMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from dashboard.mixins import AdminOrInstructorMixin
from result.mixins import ResultReleaseForbiddenMixin
from student.models import Student
from .forms import StudentCAFormSet, StudentExamFormSet, CheckResultForm
from result.models import StudentCA, StudentExam, StudentResult
from course.models import Module, Course
from exam.models import CA, Exam
from .tables import StudentCATable, StudentExamTable, GradeTable
from result.models import Grade
from . import utils
from result.tables import StudentCATable as StudentResultCATable
from result.tables import StudentExamTable as StudentResultExamTable

BATCH = get_current_batch()

class Dashboard(LoginRequiredMixin, PermissionRequiredMixin, SingleTableView):
    permission_required = 'admin'
    model = Grade
    table_class = GradeTable
    template_name = 'dashboard/result/dashboard.html'
    #release result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_result_released'] = utils.is_result_released()
        return context
    

class CreateGrade(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'admin'
    model = Grade
    fields = '__all__'
    template_name = 'general/general_form.html'
    success_message = 'Grade was added successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add new grade'
        return context

class UpdateGrade(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'admin'
    model = Grade
    fields = '__all__'
    template_name = 'general/general_form.html'
    success_message = 'Grade was updated successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit grade'
        return context

class DeleteGrade(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'admin'
    model = Grade
    template_name = 'general/general_confirm_delete.html'
    success_url = reverse_lazy('result_dashboard:dashboard')
    success_message = 'Subject ({}) deleted successfully'

class ReleaseResult(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'admin'
    template_name = 'dashboard/result/release_result.html'

    def post(self, request, *args, **kwargs):
        courses = Course.objects.filter(live=True)
        for course in courses:
            utils.generate_result(course)
        messages.success(request, 'Result released successfully')
        return redirect(reverse('result_dashboard:dashboard'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CheckResult(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'admin'
    form = CheckResultForm
    template_name = 'dashboard/result/check_result.html'

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            student = Student.objects.get(user__email__exact=email)
            batch = form.cleaned_data.get('batch')
            course = form.cleaned_data.get('course')
            student_result = StudentResult.objects.get(student=student, course=course, batch=batch)
            return redirect(reverse('result_dashboard:student_result_view', kwargs={'pk':student_result.pk}))
        return self.render_to_response({'form':form})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form()
        context['title'] = 'Check Student result'
        context['btn_text'] = 'Check result'
        return context
    

class StudentResultView(LoginRequiredMixin, PermissionRequiredMixin, MultiTableMixin, TemplateView):
    permission_required = 'admin'
    template_name = 'dashboard/result/student_result_view.html'
       
    def dispatch(self, request, pk, *args, **kwargs):
        self.result = get_object_or_404(StudentResult, pk=pk)
        return super().dispatch(request, *args, **kwargs)
    
    def get_tables(self):
        return [
            StudentResultCATable(self.result.cas.all()),
            StudentResultExamTable(self.result.exams.all()),
        ]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['result'] = self.result
        context['parent_url'] = reverse('result_dashboard:check_result')
        return context
    

class ModuleCAResult(AdminOrInstructorMixin, SingleTableView):
    template_name = 'dashboard/result/module_ca_result.html'
    table_class = StudentCATable

    def dispatch(self, request, module_id, ca_id, *args, **kwargs):
        self.module = get_object_or_404(Module, id=module_id)
        self.ca = get_object_or_404(CA, id=ca_id)
        self.course = self.module.course
        self.batch = BATCH
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return StudentCA.objects.filter(module=self.module,course=self.course,batch=self.batch,ca=self.ca)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_count"] = self.get_queryset().count()
        context["marked_count"] = self.get_queryset().filter(marked=True).count()
        context["unmarked_count"] = self.get_queryset().filter(marked=False).count()
        context['course'] = self.course
        context['module'] = self.module
        context['ca'] = self.ca
        context['batch'] = self.batch
        context['parent_url'] = reverse('course_dashboard:content_list', kwargs={'module_id': self.module.id})
        return context

class MarkStudentCA(AdminOrInstructorMixin, ResultReleaseForbiddenMixin, TemplateView):
    template_name = 'dashboard/result/mark_student_ca.html'
    formset = StudentCAFormSet

    def dispatch(self, request, pk, *args, **kwargs):
        self.batch = BATCH
        self.obj = get_object_or_404(StudentCA, pk=pk)
        self.redirect_to = reverse('result_dashboard:module_ca_result', kwargs={'module_id': self.obj.module.id, 'ca_id':self.obj.ca.id})
        return super().dispatch(request, pk *args, **kwargs)

    def post(self, request, pk, *args, **kwargs):
        formset = self.formset(instance=self.obj, data=request.POST)
        if formset.is_valid():
            formset.save()
            self.obj.marked = True
            self.obj.save()
            messages.success(request, 'CA marked successfull')
            return redirect(self.redirect_to)
        return render(request, self.template_name, {'formset':formset, 'obj':self.obj, 'parent_url': self.redirect_to})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = self.formset(instance=self.obj) 
        context['obj'] = self.obj
        context['parent_url'] = self.redirect_to
        return context

#Exam
class CourseExamResult(AdminOrInstructorMixin, SingleTableView):
    template_name = 'dashboard/result/module_ca_result.html'
    table_class = StudentExamTable

    def dispatch(self, request, course_id, exam_id, *args, **kwargs):
        self.course = get_object_or_404(Course, id=course_id)
        self.exam = get_object_or_404(Exam, id=exam_id)
        self.batch = BATCH
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return StudentExam.objects.filter(course=self.course,batch=self.batch,exam=self.exam)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_count"] = self.get_queryset().count()
        context["marked_count"] = self.get_queryset().filter(marked=True).count()
        context["unmarked_count"] = self.get_queryset().filter(marked=False).count()
        context['course'] = self.course
        context['exam'] = self.exam
        context['batch'] = self.batch
        context['parent_url'] = reverse('exam_dashboard:course_exam', kwargs={'pk':self.course.pk})
        return context

class MarkStudentExam(AdminOrInstructorMixin, ResultReleaseForbiddenMixin, TemplateView):
    template_name = 'dashboard/result/mark_student_ca.html'
    formset = StudentExamFormSet

    def dispatch(self, request, pk, *args, **kwargs):
        self.batch = BATCH
        self.obj = get_object_or_404(StudentExam, pk=pk)
        self.redirect_to = reverse('result_dashboard:course_exam_result', kwargs={'course_id': self.obj.course.id, 'exam_id':self.obj.exam.id})
        return super().dispatch(request, pk *args, **kwargs)

    def post(self, request, pk, *args, **kwargs):
        formset = self.formset(instance=self.obj, data=request.POST)
        if formset.is_valid():
            formset.save()
            self.obj.marked = True
            self.obj.save()
            messages.success(request, 'Exam marked successfull')
            return redirect(self.redirect_to)
        return render(request, self.template_name, {'formset':formset, 'obj':self.obj, 'parent_url': self.redirect_to})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = self.formset(instance=self.obj) 
        context['obj'] = self.obj
        context['parent_url'] = self.redirect_to
        return context