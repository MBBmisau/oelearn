from django.forms import ValidationError
from django.forms.models import inlineformset_factory
from django import forms
from academic.models import Batch
from course.models import Course
from dashboard.result.utils import is_result_released

from result.models import StudentCA, StudentCAQuestion, StudentExam, StudentExamQuestion, StudentResult
from student.models import Student

StudentCAFormSet = inlineformset_factory(StudentCA, StudentCAQuestion, fields=['score'], extra=0, can_delete=False)

StudentExamFormSet = inlineformset_factory(StudentExam, StudentExamQuestion, fields=['score'], extra=0, can_delete=False)

class CheckResultForm(forms.Form):
    email = forms.EmailField()
    batch = forms.ModelChoiceField(queryset=Batch.objects.all())
    course = forms.ModelChoiceField(queryset=Course.objects.all())

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            student = Student.objects.get(user__email__exact=email)
        except Student.DoesNotExist:
            raise ValidationError('Student with a given email is not found!')
        return email
    
    def clean_batch(self):
        batch = self.cleaned_data.get('batch')
        if not is_result_released(batch):
            raise ValidationError('Released result for selected Batch is not found')
        return batch
    
    def clean(self):
        email = self.cleaned_data.get('email')
        batch = self.cleaned_data.get('batch')
        course = self.cleaned_data.get('course')
        try:
            student = Student.objects.get(user__email__exact=email)
            result = StudentResult.objects.get(student=student, course=course, batch=batch)
        except (StudentResult.DoesNotExist, Student.DoesNotExist):
            raise ValidationError('Student result for selected Batch and Course is not found.')
        return self.cleaned_data