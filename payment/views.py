from django.shortcuts import render, get_object_or_404, redirect
from academic.mixins import CurrentBatchLiveMixin
from certificate.models import Certificate
from paystack.api.signals import successful_payment_signal
from django.dispatch import receiver
from  django.views.generic.base import TemplateView
from django.views.generic import DetailView
from django.contrib import messages
from django.urls import reverse

from custom_auth.models import CustomUser
from result.models import StudentResult

from .models import Invoice, InvoicePaymentReferrence, Order, OrderPaymentReferrence
from academic.utils import get_current_batch
from . import utils
from student.mixins import StudentTestMixin
from course.models import Course
from product.models import Product
from academic.mixins import CurrentBatchLiveMixin

@receiver(successful_payment_signal)
def on_successful_payment(sender, data, **kwargs):
    reference = data['reference']
    amount = data['amount']
    try:
        ref = InvoicePaymentReferrence.objects.get(ref=reference)
        
    except:
        ref = OrderPaymentReferrence.objects.get(ref=reference)
    else:
        ref = None
    if type(ref) == InvoicePaymentReferrence:
        invoice = ref.invoice
        if amount == invoice.amount:
            invoice.payment_method = Invoice.AUTOMATIC
            invoice.is_paid = True
            invoice.save()
            ref.is_used = True
            ref.save()
    elif type(ref) == OrderPaymentReferrence:
        order = ref.order
        if amount == order.amount:
            order.payment_method = Order.AUTOMATIC
            order.is_paid = True
            order.save()
            ref.is_used = True
            ref.save()

class CourseEnrollment(StudentTestMixin, CurrentBatchLiveMixin, TemplateView):
    template_name = 'payment/registration.html'

    def dispatch(self, request, course_id):
        self.course = get_object_or_404(Course, id=course_id)
        self.student = request.user.student
        if not self.course.registration_open:
            messages.info(request, 'Registration for this course is currently closed')
            return redirect(reverse('course:nonroll_index'))
        if self.course.is_free:
            self.course.students.add(self.student)
            messages.success(request, f'You have successfully joint course {self.course}')
            return redirect(reverse('course:enroll_index'))
        self.plan = Invoice.ENROLLMENT
        self.batch = get_current_batch()
        self.invoice = utils.get_invoice(course=self.course,plan=self.plan,student=self.student,batch=self.batch)
        self.invoice.amount = self.course.price
        self.invoice.save()
        self.invoice_ref = utils.get_ref(self.invoice)
        return super().dispatch(request, course_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['invoice'] = self.invoice
        context['amount'] = self.course.price
        context['ref'] = self.invoice_ref
        context['context_plan'] = 'Enrollment'
        return context

class CertificateEnrollment(StudentTestMixin, TemplateView):
    template_name = 'payment/registration.html'

    def dispatch(self, request, result_id):
        self.result = get_object_or_404(StudentResult, id=result_id)
        self.student = self.result.student
        self.course = self.result.course
        self.batch = self.result.batch
        if self.course.is_certificate_free:
            Certificate.objects.get_or_create(result=self.result)
            messages.success(request, f'You have successfully get certificate for course {self.course}')
            return redirect(reverse('certificate:index'))
        self.plan = Invoice.CERTIFICATE
        self.invoice = utils.get_invoice(course=self.course,plan=self.plan,student=self.student,batch=self.batch)
        self.invoice.amount = self.course.price
        self.invoice.save()
        self.invoice_ref = utils.get_ref(self.invoice)
        return super().dispatch(request, result_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['invoice'] = self.invoice
        context['amount'] = self.course.certificate_price
        context['ref'] = self.invoice_ref
        context['context_plan'] = 'Certificate'
        return context
        
class BuyProduct(StudentTestMixin, TemplateView):
    template_name = 'payment/buy_product.html'

    def dispatch(self, request, pk):
        self.product = get_object_or_404(Product, pk=pk)
        self.user = request.user
        if self.product.is_free:
            self.product.users.add(self.user)
            messages.success(request, f'You have successfully subscribe {self.product}')
            return redirect(reverse('product:user_product_detail', kwargs={'pk': self.product.pk}))
        self.order = Order.objects.get_or_create(product=self.product,user=self.user,is_paid=False)[0]
        self.order.amount = self.product.price
        self.order.save()
        self.order_ref = OrderPaymentReferrence.objects.create(order=self.order)
        return super().dispatch(request, pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.order
        context['ref'] = self.order_ref
        return context
