from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput
from intl_tel_input.widgets import IntlTelInputWidget

from .models import Student

class CreateStudentForm(forms.ModelForm):
    student_in_form = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = Student
        fields = ['phone_number', 'date_of_birth', 'address', 'lga_of_origin', 'state_of_origin', 'nationality', 'passport']
        widgets = {
            #'date_of_birth': forms.SelectDateWidget()
            'phone_number': IntlTelInputWidget(preferred_countries=['ng'],default_code='ng'),
            'date_of_birth': DatePickerInput()
        }
        input_formats = {
            'date_of_birth': ['%d/%m/%Y'],
        }
