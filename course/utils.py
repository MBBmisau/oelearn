from .models import StudentCompletedModule, Module
from academic.utils import get_current_batch
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect

BATCH = get_current_batch()

def get_last_finished_module(student, course):
    last_module = StudentCompletedModule.objects.filter(student=student, course=course, batch=BATCH).order_by('module__order').last()
    return last_module

def get_next_module(student, course):
    mod_list = []
    modules = course.modules.order_by('order')
    last_module = get_last_finished_module(student, course)
    if last_module is not None:
        last_order = last_module.module.order
        for mod in modules:
            mod_list.append(mod.order)
        last_index = mod_list.index(last_order)
        try:
            next_index = last_index + 1
        except:
            next_module = Module.objects.filter(course=course,order=next_item)[0]
        next_index = last_index
        next_item = mod_list[next_index]
        next_module = Module.objects.filter(course=course,order=next_item)[0]
        return next_module
    return course.modules.first()

def validate_prev_modules(request, student, module):
    course = module.course
    first_module = course.modules.order_by('order').first()
    last_module = get_last_finished_module(student, course)
    next_module = get_next_module(student, course)
    if last_module is None and module != first_module:
        messages.info(request, 'To access module, You must complete its previous ones')
        return redirect(reverse('course:course_detail', kwargs={'module_id': first_module.pk}))
    if module != first_module:
        if last_module.order < module.order and module != next_module:
            messages.info(request, 'To access module, You must complete its previous ones')
            return redirect(reverse('course:course_detail', kwargs={'module_id': next_module.pk}))

def get_next_module_for_module(module):
    module_order = module.order
    course = module.course
    if len(course.modules.filter(order__gt=module_order).order_by('order')) > 0:
        return course.modules.filter(order__gt=module_order).order_by('order').first()
    else:
        return None

def has_next_module(module):
    return get_next_module_for_module(module) is not None

def get_prev_module_for_module(module):
    module_order = module.order
    course = module.course
    if len(course.modules.filter(order__lt=module_order).order_by('order')) > 0:
        return course.modules.filter(order__lt=module_order).order_by('order').last()
    else:
        return None

def has_prev_module(module):
    return get_prev_module_for_module(module) is not None