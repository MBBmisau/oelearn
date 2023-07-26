#from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.views import SuccessURLAllowedHostsMixin
from django.views.generic.base import RedirectView as DjangoRedirectView
from django.urls import reverse

REDIRECT_FIELD_NAME = 'next'

class RedirectView(SuccessURLAllowedHostsMixin):
    redirect_field_name = REDIRECT_FIELD_NAME

    def get_success_url(self):
        url = self.get_redirect_url()
        if url is not None and url != '':
            return url
        return super().get_success_url()

    def get_redirect_url(self):
        redirect_to = self.request.POST.get(self.redirect_field_name, self.request.GET.get(self.redirect_field_name, ''))
        url_is_safe = url_has_allowed_host_and_scheme(url=redirect_to, allowed_hosts=self.get_success_url_allowed_hosts(), require_https=self.request.is_secure())
        return redirect_to if url_is_safe else ''

class Home(DjangoRedirectView):
  #  url = reverse('login')
   url = '/account/'
