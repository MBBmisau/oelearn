from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect

from academic.mixins import CurrentBatchRequiredMixin
from academic.utils import get_current_batch
#from payment.models import Order
#from payment.utils import get_order

from custom_auth.models import CustomUser as CustomUserModel

class StudentTestMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        student = self.request.user.student
        return self.request.user.user_type == CustomUserModel.STUDENT

#class StudentAccessMixin(LoginRequiredMixin, CurrentBatchRequiredMixin, StudentTestMixin, TemplateView):
##    """
#    request user must be student
#
#    Student must not graduate, suspended, dismissed
#    Student.bath must be current Batch
#    Must pay registration
#    """
#    def get(self, request, *args, **kwargs):
#        student = self.request.user.student
#        batch = get_current_batch()
#        failed_url = reverse('student:access_denied')
#        if student.is_graduated == True:
#            messages.success(request, 'Access not granted to graduated students')
#            return redirect(failed_url)
#        if not student.batch == batch:
#            messages.success(request, 'Access denied, you are from current batch')
#            return redirect(failed_url)
#        if not student.registration_clear:
#            order = get_order(user=student.user,batch=batch,product=Order.REGISTRATION)
#            return redirect(reverse('payment:registration', kwargs={'pk': order.pk}))
#        return super().get(request, *args, **kwargs)
