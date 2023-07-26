from django import forms
from django.contrib.auth.forms import UserCreationForm
#from phonenumber_field.formfields import PhoneNumberField

from .models import CustomUser, Profile
from core.widgets import PhoneNumberWidget
from intl_tel_input.widgets import IntlTelInputWidget

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email','first_name', 'last_name')
