from django import forms
from django import forms

from academic.models import Batch
from course.models import Course
from dashboard.result.utils import is_result_released

class GetCourseCertificateForm(forms.Form):
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