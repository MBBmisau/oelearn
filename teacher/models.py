from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

from custom_auth.models import CustomUser as CustomUserModel

CustomUser = settings.AUTH_USER_MODEL

class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(blank=True, null=True)
    passport = models.ImageField(upload_to='teacher', blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    lga_of_origin = models.CharField(max_length=200, verbose_name='LGA of origin', blank=True, null=True)
    state_of_origin = models.CharField(max_length=200, blank=True, null=True)
    nationality = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        name = ''
        if self.user.middle_name is not None:
            name = '{fn} {ln} {mn} ({id})'.format(fn=self.user.first_name, ln=self.user.last_name,  mn=self.user.middle_name, id=self.user.reg_id)
        if self.user.middle_name is None:
            name = '{fn} {ln} ({id})'.format(fn=self.user.first_name, ln=self.user.last_name, id=self.user.reg_id)
        return name

    def get_full_name(self):
        name = ''
        if self.user.middle_name is not None:
            name = '{fn} {ln} {mn}'.format(fn=self.user.first_name, ln=self.user.last_name,  mn=self.user.middle_name,)
        if self.user.middle_name is None:
            name = '{fn} {ln}'.format(fn=self.user.first_name, ln=self.user.last_name,)
        return name

    def get_staff_id(self):
        return self.user.reg_id

@receiver(post_save, sender=CustomUser)
def create_teacher(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == CustomUserModel.TEACHER:
            Teacher.objects.create(user = instance)

@receiver(post_save, sender=CustomUser)
def save_teacher(sender, instance,  **kwargs):
    if instance.user_type == CustomUserModel.TEACHER:
        instance.teacher.save()
