from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from customers.models import Customer
from homepage.forms import ConfirmForm


class CustomersListView(ListView):
    queryset = Customer.objects.order_by('lead__last_name')
    template_name = 'customers/customers-list.html'
    context_object_name = 'customers'


class CustomerDetailView(DetailView):
    queryset = Customer.objects.all()
    template_name = 'customers/customers-detail.html'
    # context_object_name = 'customers'


class CustomerCreateView(UserPassesTestMixin, CreateView):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.has_perm('customers.add_customer')

    model = Customer
    fields = '__all__'
    template_name = 'customers/customers-create.html'
    success_url = reverse_lazy('customers:customers_list')


class CustomerUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.has_perm('customers.change_customer')

    model = Customer
    fields = '__all__'
    template_name = 'customers/customers-edit.html'

    def get_success_url(self):
        return reverse(
            'customers:customers_detail',
            kwargs={'pk': self.object.pk}
        )


class CustomerDeleteView(UserPassesTestMixin, DeleteView):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.has_perm('customers.delete_lead')

    model = Customer
    form_class = ConfirmForm
    template_name = 'customers/customers-delete.html'
    success_url = reverse_lazy('customers:customers_list')

