import email
from django import forms
from django.contrib.auth.forms import SetPasswordForm, AdminPasswordChangeForm
from django.contrib.auth import get_user_model, password_validation
from django.core.exceptions import ValidationError
from django.conf import settings

UserModel = get_user_model()

class UserPasswordResetForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': 'The two password fields didn’t match.',
    }
    email = forms.EmailField(label='Email', help_text='Email of a user')
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    field_order = ['email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            user = UserModel.objects.get(email__iexact=email)
            self.user = user
            return user
        except:
            raise ValidationError('User with a given email was not found')
            return

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )

        password_validation.validate_password(password2,)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user

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

    def clean_new_password2(self):
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
        fields = ['first_name', 'last_name', 'middle_name', 'email', 'gender', 'reg_id', 'is_admin',]
        labels = {
            'reg_id': 'Staff ID'
        }

class CustomUserUpdateTeacherForm(forms.ModelForm):
    user_in_form = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'middle_name', 'email', 'gender', 'reg_id', 'is_admin', 'is_active']
        labels = {
            'reg_id': 'Staff ID'
        }
