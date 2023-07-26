from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_tables2 import SingleTableView
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.conf import settings
from django.contrib.sites.models import Site
from django.views import View
#context_processors
from .models import SchoolSettings, SchoolAddress, SocialLink
from .tables import SocialLinkTable
from .forms import SchoolSettingsForm, SchoolAddressForm, CreateSocialLinkForm

class ConfigView(SingleTableView):
    model = SocialLink
    table_class = SocialLinkTable
    template_name = 'config/config.html'
    context_table_name = 'table_data'

    def get_context_data(self, **kwargs):
        site = Site.objects.get_current()
        try:
            address = SchoolAddress.objects.get(site=site)
            address_form = SchoolAddressForm(instance=address)
        except SchoolAddress.DoesNotExist:
            address_form = SchoolAddressForm
        try:
            settings = SchoolSettings.objects.get(site=site)
            school_form = SchoolSettingsForm(instance=settings)
        except SchoolSettings.DoesNotExist:
            school_form = SchoolSettingsForm


        context = super().get_context_data(**kwargs)
        context['school_settings_form'] = school_form
        context['school_settings_form_title'] = 'SCHOOL SETTINGS'
        context['head_title'] = 'Config index page'
        context['school_address_form'] = address_form
        context['school_address_form_title'] = 'SCHOOL ADDRESS'
        context['social_link_form'] = CreateSocialLinkForm
        context['social_link_form_title'] = "CREATE SOCIAL MEDIA ADDRESS"
        return context

    def get_table_pagination(self, table):
        return dict(per_page=settings.TABLE_ROWS_PER_PAGE)

class SaveSettings(View):
    try:
        site = Site.objects.get_current()
    except:
        site = None
    try:
        settings = SchoolSettings.objects.get(site=site)
        form_class = SchoolSettingsForm(instance=settings)
    except: #SchoolSettings.DoesNotExist:
        form_class = SchoolSettingsForm
        settings = None
    template_name = 'general/general_form.html'

    def get(self, request, *args, **kwargs):

        form = self.form_class
        return render(request, self.template_name, {'form':form,'title':'Schools settings',})

    def post(self, request, *args, **kwargs):
        if settings:
            form = SchoolSettingsForm(request.POST, request.FILES, instance=self.settings)
        else:
            form = SchoolSettingsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'School settings was updated successfully')
            return redirect(reverse('config:config'))
        return render(request, self.template_name, {'form':form,'title':'Schools settings',})

class SaveAddress(View):
    site = Site.objects.get_current()
    try:
        address = SchoolAddress.objects.get(site=site)
        form_class = SchoolAddressForm(instance=address)
    except SchoolAddress.DoesNotExist:
        address = None
        form_class = SchoolAddressForm
    template_name = 'general/general_form.html'

    def get(self, request, *args, **kwargs):

        form = self.form_class
        return render(request, self.template_name, {'form':form,'title':'Schools address',})

    def post(self, request, *args, **kwargs):
        if self.address is not None:
            form = SchoolAddressForm(request.POST, instance=self.address)
        else:
            form = SchoolAddressForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'School address was updated successfully')
            return redirect(reverse('config:config'))
        return render(request, self.template_name, {'form':form,'title':'Schools address',})

class CreateSocialLink(SuccessMessageMixin, CreateView):
    model = SocialLink
    fields = '__all__'
    template_name = 'general/general_form.html'
    success_message = 'Social media address was added successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add new social media link'
        return context

class UpdateSocialLink(SuccessMessageMixin, UpdateView):
    model = SocialLink
    fields = '__all__'
    template_name = 'general/general_form.html'
    success_message = 'Social media address was updated successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit social media address'
        return context

class DeleteSocialLink(SuccessMessageMixin, DeleteView):
    model = SocialLink
    template_name = 'general/general_confirm_delete.html'
    success_url = reverse_lazy('subject:subject')
    success_message = 'Social media address ({}) deleted successfully'
