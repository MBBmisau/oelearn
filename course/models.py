from email.policy import default
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.forms import ValidationError
from django.template.loader import render_to_string
from django.urls import reverse
import os
from django.core.exceptions import ValidationError
from dashboard import exam

from student.models import Student
from teacher.models import Teacher
from academic.models import Batch
from academic.utils import get_current_batch

class Subject(models.Model):
    title = models.CharField(max_length=200, help_text='Mathematics')
    short_title = models.CharField(max_length=20, help_text='Eg. MATH')

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course_dashboard:dashboard')

    def save(self, *args, **kwargs):
        self.short_title = self.short_title.upper()
        return super().save(*args, **kwargs)


class Course(models.Model):
    instructor = models.ForeignKey(Teacher,  related_name="courses_to_take", on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name="courses", on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    overview = models.TextField()
    price = models.PositiveIntegerField(verbose_name='Enrollment price', null=True, blank=True)
    is_free = models.BooleanField(default=False)
    certificate_price = models.PositiveIntegerField(null=True, blank=True)
    is_certificate_free = models.BooleanField(default=False)
    students = models.ManyToManyField(Student, related_name="courses_joined", blank=True)
    live = models.BooleanField(default=True, help_text='Unless marked, student can not acess this course.')
    registration_open = models.BooleanField(default=True, help_text='Unless marked, students can not register this course')
    exam_open = models.BooleanField(default=False, help_text='Unless marked, Students can not take Exam related to this Course')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def num_modules(self):
        return self.modules.all().count()

    def num_students(self):
        return self.students.all().count()

    def num_students_completed(self):
        #return students_completed in current batch
        batch = get_current_batch()
        try:
            return self.students_completed.filter(batch=batch).count()
        except Exception as e:
            return 0

    def has_modules(self):
        return self.num_modules() > 0

    def primary_module(self):
        return self.modules.first()

    def primary_module_id(self):
        module = self.primary_module()
        return module.id
    
    def clean(self):
        if self.is_free and self.price:
            raise ValidationError('Free course must not have a price')
        if self.is_certificate_free and self.certificate_price:
            raise ValidationError('Course with free certificate must not have certificate price')
        if not self.is_free and not self.price:
            raise ValidationError('Course must either be free or have enrollment price')
        if not self.is_certificate_free and not self.certificate_price:
            raise ValidationError('Course must either have free certificate or have certificate price')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course_dashboard:dashboard')

class Module(models.Model):
    course = models.ForeignKey(Course, related_name="modules", on_delete=models.CASCADE)
    title = models.CharField(max_length=200, help_text='Eg. Introduction')
    sub_title = models.CharField(max_length=200, help_text='Eg. Week 1')
    order = models.PositiveIntegerField(help_text='Eg. assign 1 to week 1, 2 to week 2 etc')
    description = models.TextField(blank=True)
    live = models.BooleanField(default=False, help_text='If marked, students can access contents and assessment attached to this module')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.order}, {self.title}'

    def num_contents(self):
        return self.contents.filter(live=True).count()

    def num_assessments(self):
        return self.assessments.filter(live=True).count()


class Content(models.Model):
    module = models.ForeignKey(Module, related_name="contents", on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in': (
        'text', 'video', 'image', 'file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    live = models.BooleanField(default=False)
    order = models.PositiveIntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.item.title


class ItemBase(models.Model):
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    #def render(self):
    #    return render_to_string(
    #        f'courses/content/{self._meta.model_name}.html', {'item': self}
    #    )


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='files')
    size = models.IntegerField()
    format = models.CharField(max_length=50)

    @property
    def file_extension(self):
        return os.path.splitext(self.file.path)[1][1:]

    def save(self, *args, **kwargs):
        self.size = self.file.size
        self.format = self.file_extension
        return super().save(*args, **kwargs)

class Image(ItemBase):
    image = models.ImageField(upload_to='images')


class Video(ItemBase):
    url = models.URLField(blank=True,null=True)
    video_file = models.FileField(upload_to='content/video', blank=True, null=True)
    
    def is_file(self):
        if self.video_file:
            return True
            
    def is_url(self):
        if self.url:
            return True
            
    def clean(self):
        if self.url and self.video_file:
            raise ValidationError('Video either have url or file but not all')

class StudentCompletedCourse(models.Model):
    student = models.ForeignKey(Student, related_name='couses_completed', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='students_completed_course', on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'course', 'batch')

class StudentCompletedModule(models.Model):
    student = models.ForeignKey(Student, related_name='models_completed', on_delete=models.CASCADE)
    module = models.ForeignKey(Module, related_name='students_completed_module', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='students_completed_course_module', on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['module__order']
        unique_together = ('student', 'module', 'batch')

    def save(self, *args, **kwargs):
        if not self.course:
            self.course = self.module.course
        return super().save(*args, **kwargs)
