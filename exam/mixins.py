from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

class ExamOpenMixin:
    def dispatch(self, request, *args, **kwargs):
        if not self.course.exam_open:
            messages.success(request, 'This Exam is temporarily unavailable')
            return redirect(reverse('course:enroll_index'))
        return super().dispatch(request, *args, **kwargs)