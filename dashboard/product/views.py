from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from product.models import Product

class Dashboard(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'admin'
    template_name = 'dashboard/product/dashboard.html'
    model = Product
    context_object_name = 'products'

class CreateProduct(LoginRequiredMixin, SuccessMessageMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'admin'
    model = Product
    exclude = ['users',]
    fields = ['title','description','is_free','price','live','downloadable','file','image']
    template_name = 'general/general_form.html'
    success_message = 'Product was added successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add new product'
        return context

class UpdateProduct(LoginRequiredMixin, SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'admin'
    model = Product
    #exclude = ['users',]
    fields = ['title','description','is_free','price','live','downloadable','file','image']
    template_name = 'general/general_form.html'
    success_message = 'Product was updated successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit product'
        return context

class DeleteProduct(LoginRequiredMixin, SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'admin'
    model = Product
    template_name = 'general/general_confirm_delete.html'
    success_url = reverse_lazy('product_dashboard:dashboard')
    success_message = 'Product ({}) deleted successfully'