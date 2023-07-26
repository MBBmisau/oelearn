from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string
import random

from academic.models import Batch
from certificate.models import Certificate
from result.models import StudentResult
from student.models import Student
from course.models import Course
from academic.utils import get_current_batch
from product.models import Product

BATCH = get_current_batch()

class Transaction(models.Model):
    CREDIT, DEBIT = 'credit', 'debit'
    TXN_TYPE_CHOICES = [
        (CREDIT, 'Credit'),
        (DEBIT, 'Debit')
    ]
    txn_type = models.CharField(verbose_name='Type', choices=TXN_TYPE_CHOICES, max_length=128)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(verbose_name="Amount", decimal_places=2, max_digits=12)
    date_created = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)

    def __str__(self):
        return f'{self.txn_type} | {self.amount}'

    class Meta:
        ordering = ['-date_created',]

    def clean(self):
        # make sure credit translation does not have funding_partner
        if self.txn_type == self.DEBIT and self.funding_partner is not None:
            pass
        #    raise ValidationError('Debit translation should not have a funding partner')

class Invoice(models.Model):
    ENROLLMENT, CERTIFICATE = 'enrollment', 'certificate'
    PLAN_CHOICES = [
        (ENROLLMENT, 'enrollment'),
        (CERTIFICATE, 'certificate'),
    ]
    MANUAL, AUTOMATIC = 'manual', 'automatic'
    PAYMENT_METHOD_CHOICES = [
        (AUTOMATIC, 'Automatic'),
        (MANUAL, 'Manual')
    ]
    invoice_id = models.CharField(max_length=250, unique=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    plan = models.CharField(max_length=100, choices=PLAN_CHOICES)
    amount = models.PositiveIntegerField(null=True)
    is_paid = models.BooleanField(default=False)
    batch = models.ForeignKey(Batch, on_delete=models.PROTECT, related_name='orders')
    payment_method = models.CharField(max_length=250, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True)
    date_created = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course', 'plan', 'batch')

    def save(self, *args, **kwargs):
        if not self.invoice_id:
            self.invoice_id = random.randint(1000, 999999)
        if self.plan == self.ENROLLMENT:
            if not self.amount:
                self.amount = self.course.price
            if self.is_paid and self.batch == BATCH:
                self.course.students.add(self.student)
                self.course.save()
        if self.plan == self.CERTIFICATE:
            if not self.amount:
                self.amount = self.course.certificate_price
            if self.is_paid:
                result = StudentResult.objects.get(course=self.course,batch=self.batch,student=self.student)
                cert = Certificate.objects.get_or_create(result=result)
        return super().save(*args, **kwargs)
        
class Order(models.Model):
    MANUAL, AUTOMATIC = 'manual', 'automatic'
    PAYMENT_METHOD_CHOICES = [
        (AUTOMATIC, 'Automatic'),
        (MANUAL, 'Manual')
    ]
    order_id = models.CharField(max_length=250, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(null=True)
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=250, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True)
    date_created = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = random.randint(10000, 9999999)
        if not self.amount:
            self.amount = self.product.price
        if self.is_paid:
            self.product.users.add(self.user)
            self.product.save()
        return super().save(*args, **kwargs)

class InvoicePaymentReferrence(models.Model):
    ref = models.CharField(max_length=250, unique=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    is_used = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ref

    def save(self, *args, **kwargs):
        if not self.ref:
            self.ref = get_random_string().upper()
        return super().save(*args, **kwargs)
        
class OrderPaymentReferrence(models.Model):
    ref = models.CharField(max_length=250, unique=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    is_used = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ref

    def save(self, *args, **kwargs):
        if not self.ref:
            self.ref = get_random_string().lower()
        return super().save(*args, **kwargs)
