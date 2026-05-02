from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView, ListView

from .forms import ProductForm
from .models import Product
from .tasks import check_price


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            check_price.delay(product.pk)
            return redirect('product_list')
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


class ProductDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk, user=request.user)
        product.delete()
        return redirect('product_list')


class ProductCheckView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk, user=request.user)
        check_price.delay(product.pk)
        return redirect('product_list')
    

class ProductHistoryDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'products/product_history.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)