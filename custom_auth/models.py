from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin,
)

#from student.generators import generate_admission_no

class MyUserManager(BaseUserManager):

    def create_user(self, email, reg_id, user_type, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """

        if not email:
            raise ValueError('The given email must be set')

        user = self.model(
            reg_id=reg_id, email=email, user_type=user_type, **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_type, reg_id, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given reg_id, user_type and password.
        """
        user = self.create_user(
            reg_id=reg_id, email=email,
            password=password,
            user_type=user_type, **extra_fields
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    MALE = 'm'
    FEMALE = 'f'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]
    STUDENT = '10'
    TEACHER = '20'
    #ADMIN = '30'
    USER_TYPE_CHOICES = [
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField('email address', unique=True,
        error_messages={
            'unique': "This email already exists.",
        },)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    reg_id = models.CharField(max_length=50, unique=True, blank=True, help_text='Leave blank to be generated automatically')
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type', 'reg_id',]

    def __str__(self):
        return '{}({})'.format(self.first_name, self.reg_id)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_full_name(self):
        name = ''
        if self.middle_name is not None:
            name = '{fn} {ln} {mn}'.format(fn=self.first_name, ln=self.last_name,  mn=self.middle_name)
        if self.middle_name is None:
            name = '{fn} {ln}'.format(fn=self.first_name, ln=self.last_name)
        return name

    def get_short_name(self):
        return self.first_name

    def user_type_text(self):
        if self.user_type == self.STUDENT:
            return 'Student'
        elif self.user_type == self.TEACHER:
            return 'Teacher'
        elif self.user_type == self.ADMIN:
            return 'Admin'
        else:
            return None

    def is_student(self):
        return self.user_type == self.STUDENT

    def is_teacher(self):
        return self.user_type == self.TEACHER

    #def save(self, *args, **kwargs):
    #    if self.user_type == self.STUDENT and self.reg_id is None:
    #        self.reg_id =  generate_admission_no(self.first_name)
    #    return super().save(*args, **kwargs)
