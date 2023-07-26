from django.db import models
from django.urls import reverse

class Batch(models.Model):
    name = models.CharField(max_length=100,  unique=True, help_text='Batch A')
    order = models.PositiveSmallIntegerField(help_text='eg 1 for Batch A', blank=True, null=True)
    is_current = models.BooleanField(default=False, help_text='When set to current, the current term will be overwritten', editable=False)
    live = models.BooleanField(default=False, help_text='Unless marked, Students can perform some activities in this batch')
    next_batch = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('order',)
    
    def get_absolute_url(self):
        return reverse("academic_dashboard:dashboard")
    
