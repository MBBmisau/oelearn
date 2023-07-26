from django.shortcuts import render, redirect, get_object_or_404
from  django.views.generic.base import TemplateView, View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin, PermissionRequiredMixin
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages
from django_tables2.views import SingleTableMixin, SingleTableView
from django.conf import settings
from django.contrib.auth import get_user_model
from django.views.generic import DetailView, ListView

from custom_auth.forms import CustomUserCreateTeacherForm, CustomUserUpdateTeacherForm
from .forms import TeacherForm
from main.mixins import TablePaginationMixin
from .tables import TeachersTable
from teacher.models import Teacher
from teacher.generators import generate_staff_id
from custom_auth.models import CustomUser

CustomUser = get_user_model()

class Dashboard(LoginRequiredMixin, PermissionRequiredMixin, TablePaginationMixin, SingleTableView):
    template_name = 'dashboard/teacher/dashboard.html'
    permission_required = 'admin'
    table_class = TeachersTable
    model = Teacher


class CreateTeacher(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'admin'
    template_name = 'dashboard/teacher/create_teacher.html'
    user_form = CustomUserCreateTeacherForm
    teacher_form = TeacherForm

    def post(self, request, *args, **kwargs):
        user_form = self.user_form(request.POST)
        teacher_form = self.teacher_form(request.POST, request.FILES)
        if user_form.is_valid() and teacher_form.is_valid():

            #Teacher
            phone_number = teacher_form.cleaned_data['phone_number']
            address = teacher_form.cleaned_data['address']
            lga_of_origin = teacher_form.cleaned_data['lga_of_origin']
            state_of_origin = teacher_form.cleaned_data['state_of_origin']
            nationality = teacher_form.cleaned_data['nationality']
            try:
                passport = request.FILES['passport']
            except:
                passport = None

            user = user_form.save(commit=False)

            user.is_active = True
            user.user_type = CustomUser.TEACHER
            if not user.reg_id:
                user.reg_id = generate_staff_id(user.first_name)
            user.save()

            user.teacher.phone_number = phone_number
            user.teacher.address = address
            user.teacher.lga_of_origin = lga_of_origin
            user.teacher.state_of_origin = state_of_origin
            user.teacher.nationality = nationality
            user.teacher.passport = passport
            user.teacher.save()
            return redirect('teacher_dashboard:dashboard')
        else:
            context = {'user_form':user_form, 'teacher_form':teacher_form}
            return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = self.user_form
        context['teacher_form'] = self.teacher_form
        return context

class TeacherDetail(DetailView):
    model = Teacher
    template_name = 'dashboard/teacher/teacher_detail.html'

class UpdateTeacher(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'admin'
    template_name = 'dashboard/teacher/update_teacher.html'
    user_form = CustomUserUpdateTeacherForm
    teacher_form = TeacherForm

    def get_object(self, pk):
        self.object = get_object_or_404(Teacher, id=pk)
        return self.object

    def post(self, request, pk, *args, **kwargs):
        redirect_to = request.path
        obj = self.get_object(pk)
        if 'user_in_form' in request.POST:
            user_form = self.user_form(request.POST, instance=obj.user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Teacher edited successfully')
                return redirect(reverse('teacher_dashboard:dashboard'))
            context = {'user_form':user_form,'teacher_form':self.teacher_form(instance=obj),'teacher':self.get_object(pk),}
            return render(request, self.template_name, context)

        if 'teacher_in_form' in request.POST:
            teacher_form = self.teacher_form(request.POST, request.FILES, instance=obj)
            if teacher_form.is_valid():
                teacher_form.save()
                messages.success(request, 'Teacher edited successfully')
                return redirect(reverse('teacher_dashboard:dashboard'))
            context = {'user_form':self.user_form(instance=obj.user),'teacher_form':teacher_form,'teacher':self.get_object(pk),}
            return render(request, self.template_name, context)
        user_form = self.user_form(instance=obj.user)
        teacher_form = self.teacher_form(instance=obj)
        context = {'user_form':user_form, 'teacher_form':teacher_form,'teacher':self.get_object(pk),}
        return render(request, self.template_name, context)

    def get_context_data(self, pk, **kwargs):
        obj = self.get_object(pk)
        user_form = self.user_form(instance=obj.user)
        teacher_form = self.teacher_form(instance=obj)
        context = super().get_context_data(**kwargs)
        context['user_form'] = user_form
        context['teacher_form'] = teacher_form
        context['teacher'] = obj
        return context
