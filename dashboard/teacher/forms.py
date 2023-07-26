from django import forms
from intl_tel_input.widgets import IntlTelInputWidget

from teacher.models import Teacher

class TeacherForm(forms.ModelForm):
    teacher_in_form = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = Teacher
        fields = ['phone_number', 'address', 'lga_of_origin', 'state_of_origin', 'nationality', 'passport']
        widgets = {
            #'date_of_birth': forms.SelectDateWidget()
            'phone_number': IntlTelInputWidget(preferred_countries=['ng'],default_code='ng'),
        }
