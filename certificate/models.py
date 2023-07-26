from django.db import models

from result.models import StudentResult

class Certificate(models.Model):
    result = models.OneToOneField(StudentResult, on_delete=models.CASCADE)
    file = models.FileField(upload_to='certificate', blank=True, null=True)

    def __str__(self):
        return self.result
    
    def is_bound(self):
        if self.file:
            return True
        return False
    
    def bound_text(self):
        if self.is_bound():
            return 'Yes'
        return 'No'
    