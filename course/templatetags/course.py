from django import template

from academic.utils import get_current_batch
from course.models import StudentCompletedCourse, StudentCompletedModule
from course.utils import get_last_finished_module
from dashboard.result.utils import is_result_released
register = template.Library()

BATCH = get_current_batch()

@register.simple_tag
def completed_modules(course, student):
    return StudentCompletedModule.objects.filter(course=course,batch=BATCH,student=student).count()

@register.simple_tag
def has_completed_course_icon(course, student):
    try:
        complete = StudentCompletedCourse.objects.get(course=course,student=student,batch=BATCH)
        comp_icon = 'fas fa-check-cirle'
    except Exception as e:
        comp_icon = 'fas fa-times-circle'
    return comp_icon

@register.simple_tag
def has_completed_course(course, student):
    try:
        complete = StudentCompletedCourse.objects.get(course=course,student=student,batch=BATCH)
    except Exception as e:
        complete = None
    return complete is not None

@register.simple_tag
def is_eligible(student, module):
    course = module.course
    last_module = get_last_finished_module(student, course)
    first_module = course.modules.first()
    if module == first_module:
        return None
    if last_module is not None:
        if last_module.module.order + 1 >= module.order:
            return None
    return 'disabled'

@register.simple_tag
def is_result_released():
    if is_result_released():
        return True
    return False
