from email.policy import default
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string

from course.models import Course, Module
from dashboard import exam
from student.models import Student
from academic.models import Batch

class Exam(models.Model):
    course = models.ForeignKey(Course, related_name='exams', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in': (
        'objective', 'essay')})
    object_id = models.PositiveIntegerField()
    paper = GenericForeignKey('content_type', 'object_id')
    live = models.BooleanField(default=False)

    class Meta:
        ordering = ['course']
    
    def __str__(self):
        return self.paper.title

    #def clean(self):
        # total_marks all Exam instances must not exceed settings.MAX_EXAM_SCORE

class CA(models.Model):
    module = models.ForeignKey(Module, related_name='assessments', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in': (
        'objective', 'essay', 'assignment')})
    object_id = models.PositiveIntegerField()
    paper = GenericForeignKey('content_type', 'object_id')
    live = models.BooleanField(default=False)

    class Meta:
        ordering = ['module']

    def __str__(self):
        return self.paper.title

    #def clean(self):
        # total_marks all CA instances must not exceed settings.MAX_CA_SCORE

class PaperBase(models.Model):
    title = models.CharField(max_length=250)
    instruction = models.CharField(help_text='Eg. Answer all question', max_length=250)
    total_marks = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def num_questions(self):
        return self.questions.all().count()

    def render(self):
        return render_to_string(
            f'exam/paper/{self._meta.model_name}.html', {'paper': self}
        )

class Objective(PaperBase):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        ordering = ['-start_time']

class ObjectiveQuestion(models.Model):
    objective = models.ForeignKey(Objective, related_name='questions', on_delete=models.CASCADE)
    question_no = models.PositiveIntegerField(verbose_name='Question Number')
    question = models.CharField(max_length=255)
    optionA = models.CharField(max_length=100)
    optionB = models.CharField(max_length=100)
    optionC = models.CharField(max_length=100)
    optionD = models.CharField(max_length=100)
    answer = models.CharField(max_length=200, help_text='eg. A')
    marks = models.IntegerField(default=0)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ['question_no']

class Essay(PaperBase):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        ordering = ['-start_time']

class EssayQuestion(models.Model):
    essay = models.ForeignKey(Essay, related_name='questions', on_delete=models.CASCADE)
    question_no = models.PositiveIntegerField(verbose_name='Question Number')
    question = models.CharField(max_length=255)
    marks = models.IntegerField(default=0)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ['question_no']


class Assignment(PaperBase):
    pass

class AssignmentQuestion(models.Model):
    essay = models.ForeignKey(Assignment, related_name='questions', on_delete=models.CASCADE)
    question_no = models.PositiveIntegerField(verbose_name='Question Number')
    question = models.CharField(max_length=255)
    marks = models.IntegerField(default=0)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ['question_no']

class StudentCompletedCA(models.Model):
    INITIAL, COMPLETED_GET, COMPLETED_POST = 0, 1, 2
    COMPLETED_CHOICES = [
        (INITIAL, 'Initial'),
        (COMPLETED_GET, 'Complete Get'),
        (COMPLETED_POST, 'Complete Post'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    ca = models.ForeignKey(CA, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    completed = models.PositiveIntegerField(choices=COMPLETED_CHOICES, default=INITIAL)

class StudentCompletedExam(models.Model):
    INITIAL, COMPLETED_GET, COMPLETED_POST = 0, 1, 2
    COMPLETED_CHOICES = [
        (INITIAL, 'Initial'),
        (COMPLETED_GET, 'Complete Get'),
        (COMPLETED_POST, 'Complete Post'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    completed = models.PositiveIntegerField(choices=COMPLETED_CHOICES, default=INITIAL)
