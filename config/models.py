from django.db import models
from django.contrib.sites.models import Site
from django.urls import reverse

class SchoolSettings(models.Model):
    site = models.OneToOneField(Site, on_delete=models.CASCADE)
    school_name = models.CharField(max_length=255, help_text='The official name of the school')
    short_name = models.CharField(max_length=10, help_text='The short name for school. It must not be morethan 10 characters')
    school_section = models.CharField(max_length=255, help_text='eg. Senior Secondary School')
    school_motto = models.CharField(max_length=255)
    school_logo = models.ImageField(upload_to='school')

    def __str__(self):
        return self.school_name

    def get_absolute_url(self):
        return reverse('config:config')

    def save(self, *args, **kwargs):
        self.site = Site.objects.get_current()
        return super().save(*args, **kwargs)

class SocialLink(models.Model):
    name = models.CharField(max_length=50, help_text='eg. Facebook', unique=True)
    icon = models.CharField(max_length=25, help_text='eg. fab fa-facebook')
    color_code = models.CharField(max_length=10, help_text='HTML color code. eg #ffffff for white')
    url = models.URLField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('config:config')

class SchoolAddress(models.Model):
    site = models.OneToOneField(Site, on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    lga = models.CharField(max_length=100, verbose_name='L.G.A')
    address = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=20)
    alt_phone_number = models.CharField(max_length=20, help_text='Alternate phone number')
    email = models.EmailField()
    social_links = models.ManyToManyField(SocialLink)

    def __str__(self):
        return f'{self.email}'

    def get_absolute_url(self):
        return reverse('config:config')

    def save(self, *args, **kwargs):
        self.site = Site.objects.get_current()
        return super().save(*args, **kwargs)
