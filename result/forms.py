from django import forms
from django import forms

from academic.models import Batch
from course.models import Course
from dashboard.result.utils import is_result_released
from .models import StudentResult
from student.models import Student

class CheckResultForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        return super().__init__(*args, **kwargs)

    batch = forms.ModelChoiceField(queryset=Batch.objects.all())
    course = forms.ModelChoiceField(queryset=Course.objects.all())
    
    def clean_batch(self):
        batch = self.cleaned_data.get('batch')
        if not is_result_released(batch):
            raise forms.ValidationError('Released result for selected Batch is not found')
        return batch
    
    def clean(self):
        batch = self.cleaned_data.get('batch')
        course = self.cleaned_data.get('course')
        try:
            student = self.user.student
            result = StudentResult.objects.get(student=student, course=course, batch=batch)
        except (StudentResult.DoesNotExist):
            raise forms.ValidationError('Your result for selected Batch and Course is not found.')
        return self.cleaned_data
    
class VerifyResultForm(forms.Form):
    reg_id = forms.CharField(label='Registration number', max_length=150)
    batch = forms.ModelChoiceField(queryset=Batch.objects.all())
    course = forms.ModelChoiceField(queryset=Course.objects.all())

    def clean_reg_id(self):
        reg_id = self.cleaned_data.get('reg_id')
        try:
            student = Student.objects.get(user__reg_id__exact=reg_id)
        except Student.DoesNotExist:
            raise forms.ValidationError('Student with a given Registration number is not found!')
        return reg_id
    
    def clean_batch(self):
        batch = self.cleaned_data.get('batch')
        if not is_result_released(batch):
            raise forms.ValidationError('Released result for selected Batch is not found')
        return batch
    
    def clean(self):
        reg_id = self.cleaned_data.get('reg_id')
        batch = self.cleaned_data.get('batch')
        course = self.cleaned_data.get('course')
        try:
            student = Student.objects.get(user__reg_id__exact=reg_id)
            result = StudentResult.objects.get(student=student, course=course, batch=batch)
        except (StudentResult.DoesNotExist, Student.DoesNotExist):
            raise forms.ValidationError('Student result for selected Batch and Course is not found.')
        return self.cleaned_data