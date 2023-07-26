from django import forms

from .models import SchoolSettings, SchoolAddress, SocialLink

class SchoolSettingsForm(forms.ModelForm):
    class Meta:
        model = SchoolSettings
        fields = '__all__'
        exclude = ('site',)

class SchoolAddressForm(forms.ModelForm):
    class Meta:
        model = SchoolAddress
        fields = '__all__'
        exclude = ('site',)
    
class CreateSocialLinkForm(forms.ModelForm):
    class Meta:
        model = SocialLink
        fields = '__all__'