from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from customers.models import Customer
from homepage.forms import ConfirmForm


class CustomersListView(ListView):
    queryset = Customer.objects.select_related('lead', 'contract').order_by('lead__last_name')
    template_name = 'customers/customers-list.html'
    context_object_name = 'customers'


class CustomerDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'customers.view_customer'
    queryset = Customer.objects.select_related('lead', 'contract')
    template_name = 'customers/customers-detail.html'


class CustomerCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'customers.add_customer'

    model = Customer
    fields = '__all__'
    template_name = 'customers/customers-create.html'
    success_url = reverse_lazy('customers:customers_list')


class CustomerUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'customers.change_customer'

    model = Customer
    fields = '__all__'
    template_name = 'customers/customers-edit.html'

    def get_success_url(self):
        return reverse(
            'customers:customers_detail',
            kwargs={'pk': self.object.pk}
        )


class CustomerDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'customers.delete_customer'

    model = Customer
    form_class = ConfirmForm
    template_name = 'customers/customers-delete.html'
    success_url = reverse_lazy('customers:customers_list')
