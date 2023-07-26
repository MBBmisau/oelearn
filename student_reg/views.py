from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import View, TemplateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail
from django.contrib.auth import login, get_user_model
from django.http import JsonResponse
from django.conf import settings

from academic.utils import get_current_batch
from academic.mixins import CurrentBatchRequiredMixin
from student.models import Student
from student.forms import CreateStudentForm
from .tokens import account_activation_token
from custom_auth.forms import CustomUserForm
from custom_auth.models import CustomUser
#from payment.models import Order
from student.generators import generate_admission_no, generate_admission_no_orl

BATCH = get_current_batch()

class Register(TemplateView):
    template_name = 'student_reg/register.html'
    user_form = CustomUserForm
    student_form = CreateStudentForm

    def post(self, request, *args, **kwargs):
        user_form = self.user_form(request.POST)
        student_form = self.student_form(request.POST, request.FILES)
        if user_form.is_valid() and student_form.is_valid():

            #Student
            phone_number = student_form.cleaned_data['phone_number']
            date_of_birth = student_form.cleaned_data['date_of_birth']
            address = student_form.cleaned_data['address']
            lga_of_origin = student_form.cleaned_data['lga_of_origin']
            state_of_origin = student_form.cleaned_data['state_of_origin']
            nationality = student_form.cleaned_data['nationality']

            passport = request.FILES['passport']

            user = user_form.save(commit=False)
            user.is_active = True
            user.user_type = CustomUser.STUDENT
            user.reg_id =  generate_admission_no(user.first_name)
            user.save()

            user.student.phone_number = phone_number
            user.student.date_of_birth = date_of_birth
            user.student.address = address
            user.student.lga_of_origin = lga_of_origin
            user.student.state_of_origin = state_of_origin
            user.student.nationality = nationality
            user.student.passport = passport
            user.student.start_batch = BATCH

            user.reg_id = generate_admission_no_orl(user.student)
            user.save()
            user.student.save()
            
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            messages.success(request, 'Account created succesfully')
            return redirect(reverse('student:dashboard'))

            #current_site = get_current_site(request)
            #school_name = settings.SCHOOL_NAME
            #subject = f'Activate your {school_name} account'
            #message = render_to_string('email/account_activation.html', {
             #   'user':user,
              #  'domain':current_site.domain,
               # 'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                #'token':account_activation_token.make_token(user),
            #})
            #from_email = 'alhudaacademyonline@gmail.com'
            #to_email = user_form.cleaned_data.get('email')
            #email = EmailMessage(subject, message, to=[to_email])
            #email.send()
            #send_mail(subject, message, from_email=from_email, recipient_list=[to_email])
            #messages.success(request, 'Please! Confirm your email to complete #your registration')

            #return redirect('student_reg:success')
        else:
            context = {'user_form':user_form, 'student_form':student_form}
            return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = self.user_form
        context['student_form'] = self.student_form
        return context

def validate_email(request):
    email = request.GET.get('email', None)
    data = {
        'is_taken': get_user_model().objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(data)

class Success(TemplateView):
    template_name = 'student_reg/success.html'

class Activate(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:

            uid = urlsafe_base64_decode(uidb64)
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Your account has been confirmed')
            return redirect(reverse('student:dashboard'))
        else:
            messages.warning(request, 'The confirmation link was invalid')
            return redirect('student_reg:invalid_activation_link')

class InvalidActivationLink(TemplateView):
    template_name = 'student_reg/invalid_activation_link.html'

def dashboard(request):
    template_name = 'student_reg/dashboard.html'
    context = {}

    return render(request, template_name, context)

@login_required
def profile(request):
    template_name = 'customer/profile.html'
    context = {}

    context['user'] = request.user
    context['profile'] = request.user.profile

    return render(request, template_name, context)

@login_required
def profile_update(request):
    template_name = 'customer/profile_update.html'
    context = {}

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile updated successfully')

            return redirect('customer:dashboard')
        elif u_form.is_valid():
            u_form.save()
            messages.success(request, 'Profile updated successfully')

            return redirect('customer:dashboard')
        elif p_form.is_valid():
            p_form.save()

            messages.success(request, 'Profile updated successfully')

            return redirect('customer:dashboard')
        else:
            context['u_form'] = UserUpdateForm()
            context['p_form'] = ProfileUpdateForm()
            context['user'] = request.user
            context['profile'] = request.user.profile
            return render(request, template_name, context)
    else:
        context['u_form'] = UserUpdateForm()
        context['p_form'] = ProfileUpdateForm()
        context['user'] = request.user
        context['profile'] = request.user.profile
        return render(request, template_name, context)
