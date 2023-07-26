from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField

from custom_auth.models import CustomUser as CustomUserModel
from academic.models import  Batch

CustomUser = settings.AUTH_USER_MODEL

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(null=True, blank=True)
    passport = models.ImageField(upload_to='student', null=True, blank=True)
    date_of_birth = models.DateField(help_text='YYYY-MM-DD', null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    lga_of_origin = models.CharField(max_length=200, verbose_name='LGA of origin', null=True, blank=True)
    state_of_origin = models.CharField(max_length=200, null=True, blank=True)
    nationality = models.CharField(max_length=200, null=True, blank=True)
    start_batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True)
    date_joint = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_joint']

    def __str__(self):
        return self.user.get_full_name()

    def get_admission_number(self):
        return self.user.reg_id

    def get_full_name(self):
        return self.user.get_full_name()

@receiver(post_save, sender=CustomUser)
def create_student(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == CustomUserModel.STUDENT:
            Student.objects.create(user = instance)

@receiver(post_save, sender=CustomUser)
def save_student(sender, instance,  **kwargs):
    if instance.user_type == CustomUserModel.STUDENT:
        instance.student.save()