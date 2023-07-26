from django.shortcuts import render, redirect, get_object_or_404
from  django.views.generic.base import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.contrib import messages
from .forms import GetStudentForm
from django_tables2.views import SingleTableView
from django.contrib.auth import get_user_model
from django.views.generic import DetailView
from django.views.generic.base import TemplateResponseMixin
from django_weasyprint.views import WeasyTemplateResponseMixin
from django.views.generic.list import ListView
from django.utils import timezone

from custom_auth.forms import CustomUserForm, CustomUserUpdateStudentForm
from student.forms import CreateStudentForm
from .forms import DownloadStudentDataForm
from student.models import Student
from main.mixins import TablePaginationMixin
from .tables import StudentTable
from custom_auth.models import CustomUser
from student.generators import generate_admission_no

CustomUser = get_user_model()

class Dashboard(LoginRequiredMixin, PermissionRequiredMixin, TablePaginationMixin, SingleTableView):
    template_name = 'dashboard/student/dashboard.html'
    permission_required = 'admin'
    table_class = StudentTable
    model = Student

class GetStudent(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'admin'
    form = GetStudentForm
    template_name = 'result/check_result.html'

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            student = Student.objects.get(user__email__exact=email)
            return redirect(reverse('student_dashboard:student_detail', kwargs={'pk':student.pk}))
        return self.render_to_response({'form':form,'meta_title':'Student | Get student','title':'Get student','btn_text':'Check'})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form()
        context['meta_title'] = 'Student | Get student'
        context['title'] = 'Get student'
        context['btn_text'] = 'Check'
        return context

class CreateStudent(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'admin'
    template_name = 'dashboard/student/create_student.html'
    user_form = CustomUserForm
    student_form = CreateStudentForm

    def post(self, request, *args, **kwargs):
        user_form = self.user_form(request.POST)
        student_form = self.student_form(request.POST, request.FILES)
        if user_form.is_valid() and student_form.is_valid():

            #Teacher
            phone_number = student_form.cleaned_data['phone_number']
            date_of_birth = student_form.cleaned_data['date_of_birth']
            address = student_form.cleaned_data['address']
            lga_of_origin = student_form.cleaned_data['lga_of_origin']
            state_of_origin = student_form.cleaned_data['state_of_origin']
            nationality = student_form.cleaned_data['nationality']

            try:
                passport = request.FILES['passport']
            except:
                passport = None

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
            if 'passport' in request.POST:
                user.student.passport = passport
            user.student.save()
            messages.success(request, 'Student created successfully!')
            return redirect('student_dashboard:dashboard')
        else:
            context = {'user_form':user_form, 'student_form':student_form}
            return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = self.user_form
        context['student_form'] = self.student_form
        return context

class StudentDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'admin'
    model = Student
    template_name = 'dashboard/student/student_detail.html'

class UpdateStudent(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'admin'
    template_name = 'dashboard/student/update_student.html'
    user_form = CustomUserUpdateStudentForm
    student_form = CreateStudentForm

    def get_object(self, pk):
        self.object = get_object_or_404(Student, id=pk)
        return self.object

    def post(self, request, pk, *args, **kwargs):
        redirect_to = request.path
        obj = self.get_object(pk)
        if 'user_in_form' in request.POST:
            user_form = self.user_form(request.POST, instance=obj.user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Student edited successfully')
                return redirect(reverse('student_dashboard:dashboard'))
            context = {'user_form':user_form,'student_form':self.student_form(instance=obj),'student':self.get_object(pk),}
            return render(request, self.template_name, context)

        if 'student_in_form' in request.POST:
            student_form = self.student_form(request.POST, request.FILES, instance=obj)
            if student_form.is_valid():
                student_form.save()
                messages.success(request, 'Student edited successfully')
                return redirect(reverse('student_dashboard:dashboard'))
            context = {'user_form':self.user_form(instance=obj.user),'student_form':student_form,'student':self.get_object(pk),}
            return render(request, self.template_name, context)
        user_form = self.user_form(instance=obj.user)
        student_form = self.student_form(instance=obj)
        context = {'user_form':user_form, 'student_form':student_form,'student':self.get_object(pk),}
        return render(request, self.template_name, context)

    def get_context_data(self, pk, **kwargs):
        obj = self.get_object(pk)
        user_form = self.user_form(instance=obj.user)
        student_form = self.student_form(instance=obj)
        context = super().get_context_data(**kwargs)
        context['user_form'] = user_form
        context['student_form'] = student_form
        context['student'] = obj
        return context

class DataView(LoginRequiredMixin, PermissionRequiredMixin, TemplateResponseMixin, View):
    permission_required = 'admin'
    template_name = 'general/general_form.html'
    form = DownloadStudentDataForm

    #def get_template_names(self):
     #   if self.request.method == 'GET':
      #      return 
       # return 'dashboard/student/pdf/download_data.html'

    def get(self, request, *args, **kwargs):
        form = DownloadStudentDataForm()
        return self.render_to_response({'form':form, 'button_value': 'Download', 'title':'Download Students Data','parent_url':reverse('student_dashboard:dashboard')})
    
    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name'),
            last_name = form.cleaned_data.get('last_name'),
            middle_name = form.cleaned_data.get('middle_name'),
            email = form.cleaned_data.get('email'),
            reg_id = form.cleaned_data.get('reg_id'),
            phone_number = form.cleaned_data.get('phone_number'),
            date_of_birth = form.cleaned_data.get('date_of_birth'),
            nationality = form.cleaned_data.get('nationality'),
            state_of_origin = form.cleaned_data.get('state_of_origin'),
            lga_of_origin = form.cleaned_data.get('lga_of_origin'),
            address = form.cleaned_data.get('address'),
            date_joint = form.cleaned_data.get('date_joint'),
            get_params = f'first_name={first_name[0]}&last_name={last_name[0]}&middle_name={middle_name[0]}&email={email[0]}&reg_id={reg_id[0]}&phone_number={phone_number[0]}&date_of_birth={date_of_birth[0]}&nationality={nationality[0]}&state_of_origin={state_of_origin[0]}&lga_of_origin={lga_of_origin[0]}&address={address[0]}&date_joint={date_joint[0]}'
            download_rev = reverse('student_dashboard:download_data')
            download_url = f'{download_rev}?{get_params}'
            return redirect(download_url)
        return self.render_to_response({'form':form,})

class DownloadData(LoginRequiredMixin, PermissionRequiredMixin, TemplateResponseMixin, View):
    permission_required = 'admin'
    template_name = 'dashboard/student/pdf/download_data.html'

    def get(self, request, *args, **kwargs):
        all_fields = {
                'first_name': request.GET.get('first_name'),
                'last_name': request.GET.get('last_name'),
                'middle_name': request.GET.get('middle_name'),
                'email': request.GET.get('email'),
                'reg_id': request.GET.get('reg_id'),
                'phone_number': request.GET.get('phone_number'),
                'date_of_birth': request.GET.get('date_of_birth'),
                'nationality': request.GET.get('nationality'),
                'state_of_origin': request.GET.get('state_of_origin'),
                'lga_of_origin': request.GET.get('lga_of_origin'),
                'address': request.GET.get('address'),
                #'date_joint': request.GET.get('date_joint'),
            }
        required_fields = []
        if all_fields['middle_name'] == 'None':
            all_fields['middle_name'] = ''
        for field12 in all_fields:
            if all_fields[field12] == 'True':
                required_fields.append(field12)
        return self.render_to_response({'required_fields':required_fields,'students':Student.objects.all()})

class DownloadDataView(WeasyTemplateResponseMixin, DownloadData):
    
    def get_pdf_filename(self):
        return f'studentData-{timezone.datetime.today().date()}.pdf'