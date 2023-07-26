from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from .models import Product
from .mixins import UserProductMixin

class UserProductIndex(LoginRequiredMixin, ListView):
    template_name = 'product/user_product_index.html'
    context_object_name = 'products'
    #model = Product
    
    def get_queryset(self):
        return Product.objects.filter(users=self.request.user, live=True)

class UserProductDetail(UserProductMixin, DetailView):
    template_name = 'product/user_product_detail.html'
    model = Product
    context_object_name = 'product'
    
    def dispatch(self, request, pk):
        self.product = get_object_or_404(Product, pk=pk)
        if not self.product.live:
            raise PermissionDenied()
        return super().dispatch(request, pk)

class Shop(LoginRequiredMixin, ListView):
    template_name = 'product/shop.html'
    #model = Product
    context_object_name = 'products'
    
    def get_queryset(self):
        return Product.objects.exclude(users=self.request.user, live=True)

class ProductDetail(LoginRequiredMixin, DetailView):
    template_name = 'product/product_detail.html'
    model = Product
    context_object_name = 'product'
    
    def dispatch(self, request, pk):
        self.product = get_object_or_404(Product, pk=pk)
        if not self.product.live:
            raise PermissionDenied()
        return super().dispatch(request, pk)