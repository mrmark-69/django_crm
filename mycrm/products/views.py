from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from homepage.forms import ConfirmForm
from products.models import Product


class ProductsListView(ListView):
    queryset = Product.objects.all()
    template_name = 'products/products-list.html'
    context_object_name = 'products'


class ProductDetailView(LoginRequiredMixin, DetailView):
    queryset = (
        Product.objects.all()
    )
    template_name = "products/products-detail.html"


class ProductCreateView(UserPassesTestMixin, CreateView):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.has_perm('products.add_product')

    model = Product
    fields = '__all__'
    template_name = "products/products-create.html"
    success_url = reverse_lazy("products:products_list")


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.has_perm('products.change_product')

    model = Product
    fields = '__all__'
    template_name = "products/products-edit.html"

    def get_success_url(self):
        return reverse(
            "products:product_details",
            kwargs={"pk": self.object.pk},
        )


class ProductDeleteView(UserPassesTestMixin, DeleteView):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.has_perm('products.delete_product')

    model = Product
    form_class = ConfirmForm
    success_url = reverse_lazy("products:services_list")
    template_name = "products/products-delete.html"
