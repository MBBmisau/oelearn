from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.core.exceptions import ValidationError
from django.conf import settings

UserModel = get_user_model()

class CustomUserForm(forms.ModelForm):

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput)

    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'middle_name', 'email', 'gender']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError("Password don't match")

        password_validation.validate_password(password2,)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["password1"]
        user = super().save(commit=False)
        user.set_password(password)
        if commit:
            user.save()
        return user

class CustomUserCreateTeacherForm(CustomUserForm):

    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'middle_name', 'email', 'gender','is_admin',]

class CustomUserUpdateTeacherForm(forms.ModelForm):
    user_in_form = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'middle_name', 'gender', 'reg_id', 'is_admin', 'is_active']
        labels = {
            'reg_id': 'Staff ID'
        }

class CustomUserUpdateStudentForm(forms.ModelForm):
    user_in_form = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'middle_name', 'gender', 'reg_id', 'is_active']
        labels = {
            'reg_id': 'Registration Number'
        }
