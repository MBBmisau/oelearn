from email.policy import default
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.forms import ValidationError
from django.conf import settings
from django.urls import reverse

from student.models import Student, save_student
from exam.models import Exam, CA
from academic.models import Batch
from course.models import Course, Module

class Grade(models.Model):
    name = models.CharField(max_length=4, unique=True, help_text='eg. F')
    start_score = models.SmallIntegerField(help_text='eg. 0', unique=True)
    end_score = models.SmallIntegerField(help_text='eg. 39', unique=True)
    remark = models.CharField(max_length=15, help_text='eg. Fail for F')

    class Meta:
        ordering = ('start_score',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('result_dashboard:dashboard')

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        return super().save(*args, **kwargs)

    def clean(self):
        if self.end_score > settings.MAX_TOTAL_SCORE or  self.start_score > settings.MAX_TOTAL_SCORE:
            raise ValidationError(f'The marks of every student in any subject may not exceed {settings.MAX_TOTAL_SCORE}.')
        if self.start_score >= self.end_score:
            raise ValidationError('The starting score must not be greater than or equal to ending score')

class StudentQuestion(models.Model):
    student_answer = models.TextField(null=True)
    score = models.PositiveIntegerField(default=0)
    max_possible_score = models.PositiveIntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in': (
        'objective_question', 'essay_question', 'assignment_question')})
    object_id = models.PositiveIntegerField()
    question = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True
    
    def clean(self):
        if self.score > self.question.marks:
            raise ValidationError('Score for a question must not be greater than possible score')
    
    def save(self, *args, **kwargs):
        self.max_possible_score = self.question.marks
        return super().save(*args, **kwargs)

class StudentCA(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    ca = models.ForeignKey(CA, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    max_possible_score = models.PositiveIntegerField(default=0)
    marked = models.BooleanField(default=True)

    class Meta:
        unique_together = ['student','ca','batch','module','course']
    
    def save(self, *args, **kwargs):
        if self.marked:
            self.max_possible_score = self.ca.paper.total_marks
            self.score = 0
            for question in self.questions.all():
                self.score += question.score
        return super().save(*args, **kwargs)

class StudentExam(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    max_possible_score = models.PositiveIntegerField(default=0)
    marked = models.BooleanField(default=True)

    class Meta:
        unique_together = ['student','exam','batch','course']
    
    def save(self, *args, **kwargs):
        if self.marked:
            self.max_possible_score = self.exam.paper.total_marks
            self.score = 0
            for question in self.questions.all():
                self.score += question.score
        return super().save(*args, **kwargs)

class StudentCAQuestion(StudentQuestion):
    student_ca = models.ForeignKey(StudentCA, related_name='questions', on_delete=models.CASCADE)

class StudentExamQuestion(StudentQuestion):
    student_exam = models.ForeignKey(StudentExam, related_name='questions', on_delete=models.CASCADE)

class StudentResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    cas = models.ManyToManyField(StudentCA)
    exams = models.ManyToManyField(StudentExam)
    total_ca_score = models.PositiveIntegerField(default=0)
    total_exam_score = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ['student','batch','course']
    
    def __str__(self):
        return f'{self.student}({self.course})'
    

    def total_score(self):
        if self.total_ca_score and self.total_exam_score:
            return self.total_ca_score + self.total_exam_score
        elif self.total_ca_score :
            return self.total_ca_score
        elif self.total_exam_score:
            return self.total_exam_score
        else:
            return 0

    def grade(self):
        grades = Grade.objects.all()
        total = self.total_score()
        for grade in grades:
            for x in range(grade.start_score, grade.end_score+1):
                if total == x:
                    return grade.name
                    break

        return ''

    def remark(self):
        grades = Grade.objects.all()
        total = self.total_score()
        for grade in grades:
            for x in range(grade.start_score, grade.end_score+1):
                if total == x:
                    return grade.remark
                    break

        return ''

    def get_score(self, score=None):
        if score is not None:
            return score
        else:
            return 0

    def clean(self):
        ca_score = self.get_score(self.ca_score)
        exam_score = self.get_score(self.exam_score)
        total = self.get_score(self.total_score())
        if ca_score > settings.MAX_CA_SCORE:
            raise ValidationError(f'The marks for CA must not exceed {settings.MAX_CA_SCORE}')
        if exam_score > settings.MAX_EXAM_SCORE:
            raise ValidationError(f'The marks for EXAM must not exceed {settings.MAX_EXAM_SCORE}')
        if total > settings.MAX_TOTAL_SCORE:
            raise ValidationError(f'The total marks of every student in any subject must not be greater than {settings.MAX_TOTAL_SCORE}.')

class ResultRelease(models.Model):
    batch = models.OneToOneField(Batch, on_delete=models.CASCADE)
    released = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)