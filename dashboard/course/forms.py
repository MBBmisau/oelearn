from django import forms
from django.forms.models import inlineformset_factory
from djangoformsetjs.utils import formset_media_js

from course.models import Course, Module

class BaseFormSetForm(forms.ModelForm):
    class Media(object):
        js = formset_media_js 

ModuleFormSet = inlineformset_factory(Course, Module, form=BaseFormSetForm, fields=['title', 'sub_title', 'order', 'live', 'description'], extra=1, can_delete=True)
