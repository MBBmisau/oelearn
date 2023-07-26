from django.shortcuts import render, get_object_or_404, redirect
from  django.views.generic.base import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse
from django.contrib import messages

from academic.mixins import CurrentBatchLiveMixin
from dashboard.result.utils import is_result_released

from .models import Course, Module, Video, Image, File, Text, StudentCompletedModule
from student.mixins import StudentTestMixin
from .mixins import StudentCourseMixin
from . import utils
from academic.utils import get_current_batch

BATCH = get_current_batch()

#class LiveCourseMixin():
 #   return self.course.live
    
class EnrollIndex(StudentTestMixin, TemplateView):
    template_name = 'course/enroll_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.request.user.student
        context['student'] = student
        context['courses_enrolled_count'] = student.courses_joined.all().count()
        context['enrolled_courses'] = student.courses_joined.filter(live=True)
        context['is_result_released'] = is_result_released()
        return context
        
class NonrollIndex(StudentTestMixin, TemplateView):
    template_name = 'course/nonroll_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.request.user.student
        context['student'] = student
        context['courses_enrolled_count'] = student.courses_joined.all().count()
        context['non_enrolled_courses'] = Course.objects.filter(live=True, registration_open=True).exclude(students=student)
        return context

class CourseDetail(StudentTestMixin, StudentCourseMixin, CurrentBatchLiveMixin, TemplateView):
    template_name = 'course/course_detail.html'

    def dispatch(self, request, module_id):
        self.module = get_object_or_404(Module, pk=module_id)
        self.course = self.module.course
        self.videos = []
        self.files = []
        self.images = []
        self.texts = []
        redirect_to = reverse('course:enroll_index')
        student = request.user.student
        self.student = student
        self.batch = BATCH
        if not self.module.live:
            messages.info(request, 'The module is currently closed')
            return redirect(redirect_to)
        #return utils.validate_prev_modules(request, student, self.module)
        #course = module.course
        first_module = self.course.modules.order_by('order').first()
        last_module = utils.get_last_finished_module(student, self.course)
        if not last_module is None: 
            last_module = last_module.module
        next_module = utils.get_next_module(student, self.course)
        if last_module is None and self.module != first_module:
            messages.info(request, 'To access module, You must complete its previous ones')
            return redirect(reverse('course:course_detail', kwargs={'module_id': first_module.pk}))
        if self.module != first_module:
            if last_module.order + 1 < self.module.order and self.module != next_module:
                messages.info(request, 'To access module, You must complete its previous ones')
                return redirect(reverse('course:course_detail', kwargs={'module_id': next_module.pk}))
        for content in self.module.contents.filter(live=True):
            if type(content.item) == Video:
                self.videos.append(content.item)
            elif type(content.item) == File:
                self.files.append(content.item)
            elif type(content.item) == Image:
                self.images.append(content.item)
            elif type(content.item) == Text:
                self.texts.append(content.item)
        return super().dispatch(request, module_id)

    def get(self, request, *args, **kwargs):
        clear = StudentCompletedModule.objects.get_or_create(student=self.student, module=self.module, course=self.course, batch=self.batch)[0]
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.course
        context['module'] = self.module
        context['assessments'] = self.module.assessments.filter(live=True)
        context['videos'] = self.videos
        context['files'] = self.files
        context['images'] = self.images
        context['texts'] = self.texts
        context['next_module'] = utils.get_next_module_for_module(self.module)
        context['has_next_module'] = utils.has_next_module(self.module)
        context['prev_module'] = utils.get_prev_module_for_module(self.module)
        context['has_prev_module'] = utils.has_prev_module(self.module)
        return context

    #if student does not complete previous module, deny access and redirect to supposed module
    #Student attempt Test ca once
    #module must be opened
    #student must be in course.students
