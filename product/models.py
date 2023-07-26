from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from django.urls import reverse

class Product(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    downloadable = models.BooleanField(default=True)
    file = models.FileField(upload_to='product/file', blank=True, null=True)
    image = models.ImageField(upload_to='product/image')
    price = models.PositiveIntegerField(help_text='Price in Naira', blank=True, null=True)
    is_free =  models.BooleanField(default=False)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    live = models.BooleanField(default=True, help_text='Unless marked, product will be visible to students')
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('product_dashboard:dashboard')
    
    def clean(self):
        if not self.downloadable and self.file:
            raise ValidationError('Non downloadable product must not have a file')
        if self.is_free and self.price:
            raise ValidationError('Free product must have a price')
