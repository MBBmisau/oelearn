from django import forms
from django import forms

from student.models import Student

class GetStudentForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            student = Student.objects.get(user__email__exact=email)
        except Student.DoesNotExist:
            raise forms.ValidationError('Student with a given email is not found!')
        return email

class DownloadStudentDataForm(forms.Form):
    first_name = forms.BooleanField(required=False)
    last_name = forms.BooleanField(required=False)
    middle_name = forms.BooleanField(required=False)
    email = forms.BooleanField(required=False)
    reg_id = forms.BooleanField(label='Admission Number',required=False)
    phone_number = forms.BooleanField(required=False)
    date_of_birth = forms.BooleanField(required=False)
    nationality = forms.BooleanField(required=False)
    state_of_origin = forms.BooleanField(required=False)
    lga_of_origin = forms.BooleanField(required=False)
    address = forms.BooleanField(required=False)
    #date_joint = forms.BooleanField(required=False)
