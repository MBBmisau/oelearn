from dataclasses import fields
from django import forms
from django.forms.models import inlineformset_factory
from bootstrap_datepicker_plus.widgets import DateTimePickerInput

from exam.models import Objective, ObjectiveQuestion, Essay, EssayQuestion, Assignment, AssignmentQuestion
from result.models import StudentCA, StudentCAQuestion

class ObjectiveForm(forms.ModelForm):

    class Meta:
        model = Objective
        exclude = ['created', 'updated']
        widgets = {
            'start_time': DateTimePickerInput(),
            'end_time': DateTimePickerInput()
        }
class EssayForm(forms.ModelForm):

    class Meta:
        model = Essay
        exclude = ['created', 'updated']
        widgets = {
            'start_time': DateTimePickerInput(),
            'end_time': DateTimePickerInput()
        }
class AssignmentForm(forms.ModelForm):

    class Meta:
        model = Assignment
        exclude = ['created', 'updated']

ObjectiveFormSet = inlineformset_factory(Objective, ObjectiveQuestion, fields=['question_no', 'question',
    'optionA', 'optionB', 'optionC', 'optionD', 'answer', 'marks'], extra=1, can_delete=True)

EssayFormSet = inlineformset_factory(Essay, EssayQuestion, fields=['question_no', 'question', 'marks'], extra=1, can_delete=True)

AssignmentFormSet = inlineformset_factory(Assignment, AssignmentQuestion, fields=['question_no', 'question', 'marks'], extra=1, can_delete=True)
