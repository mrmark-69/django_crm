import logging

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from .forms import AdvertisingForm, ConfirmForm
from .models import Advertising, Service, Contract, Lead

log = logging.getLogger(__name__)


class AdvertisingListView(ListView):
    template_name = 'crmapp/ads/ads-list.html'
    context_object_name = 'ads'
    queryset = (Advertising.objects.all().prefetch_related('service'))


class AdvertisingCreateView(UserPassesTestMixin, CreateView):
    def test_func(self):
        user = self.request.user
        return self.request.user.is_superuser or user.has_perm('crmapp.add_advertising')

    model = Advertising
    form_class = AdvertisingForm
    template_name = 'crmapp/ads/ads-create.html'
    success_url = reverse_lazy('crmapp:ads')

    def form_valid(self, form):
        response = super().form_valid(form)
        form.instance.created_by = self.request.user

        return response


class AdvertisingUpdateView(UpdateView):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.has_perm('crmapp.change_advertising')

    model = Advertising
    fields = '__all__'
    template_name = "crmapp/ads/ads-edit.html"

    def get_success_url(self):
        return reverse(
            "crmapp:ads_details",
            kwargs={"pk": self.object.pk},
        )


class AdvertisingDetailView(DetailView):
    queryset = Advertising.objects.all().select_related('service')
    template_name = 'crmapp/ads/ads-detail.html'


class AdvertisingDeleteView(UserPassesTestMixin, DeleteView):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.has_perm('crmapp.delete_advertising')

    model = Advertising
    success_url = reverse_lazy("crmapp:ads")
    form_class = ConfirmForm
    template_name = "crmapp/ads/ads-delete.html"


class ServicesListView(ListView):
    queryset = Service.objects.all()
    template_name = 'crmapp/products/products-list.html'
    context_object_name = 'products'


def statistic_list(request):
    return render(request, 'crmapp/ads/ads-statistic.html', context={})


class ServiceDetailView(LoginRequiredMixin, DetailView):
    queryset = (
        Service.objects.all()
    )
    template_name = "crmapp/products/products-detail.html"


class ServiceCreateView(UserPassesTestMixin, CreateView):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.has_perm('crmapp.add_service')

    model = Service
    fields = '__all__'
    template_name = "crmapp/products/products-create.html"
    success_url = reverse_lazy("crmapp:services_list")


class ServiceUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.has_perm('crmapp.change_service')

    model = Service
    fields = '__all__'
    template_name = "crmapp/products/products-edit.html"

    def get_success_url(self):
        return reverse(
            "crmapp:service_details",
            kwargs={"pk": self.object.pk},
        )


class ServiceDeleteView(UserPassesTestMixin, DeleteView):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.has_perm('crmapp.delete_service')

    model = Service
    form_class = ConfirmForm
    success_url = reverse_lazy("crmapp:services_list")
    template_name = "crmapp/products/products-delete.html"


class ContractsListView(ListView):
    template_name = 'crmapp/contracts/contracts-list.html'
    context_object_name = 'contracts'
    queryset = (Contract.objects.all().select_related('service'))


class ContractCreateView(UserPassesTestMixin, CreateView):

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.has_perm('crmapp.add_contract')

    model = Contract
    fields = '__all__'
    success_url = reverse_lazy("crmapp:contracts")
    template_name = "crmapp/contracts/contracts-create.html"


class ContractUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.has_perm('crmapp.change_contract')

    model = Contract
    fields = '__all__'
    template_name = "crmapp/contracts/contracts-edit.html"

    def get_success_url(self):
        return reverse(
            "crmapp:contracts_detail",
            kwargs={"pk": self.object.pk},
        )


class ContractDetailView(DetailView):
    queryset = (Contract.objects.all().select_related('service'))
    template_name = "crmapp/contracts/contracts-detail.html"


class ContractDeleteView(DeleteView):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.has_perm('crmapp.delete_contract')

    model = Contract
    form_class = ConfirmForm
    success_url = reverse_lazy("crmapp:contracts")
    template_name = "crmapp/contracts/contracts-delete.html"


class LeadsListView(ListView):
    template_name = 'crmapp/leads/leads-list.html'
    context_object_name = 'leads'
    queryset = (Lead.objects.all().select_related('campaign'))


class LeadCreateView(UserPassesTestMixin, CreateView):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.has_perm('crmapp.add_lead')

    model = Lead
    fields = '__all__'
    template_name = 'crmapp/leads/leads-create.html'
    success_url = reverse_lazy('crmapp:leads')


class LeadUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.has_perm('crmapp.change_lead')

    model = Lead
    fields = '__all__'
    template_name = 'crmapp/leads/leads-edit.html'

    def get_success_url(self):
        return reverse(
            'crmapp:leads_detail',
            kwargs={'pk': self.object.pk}
        )


class LeadDetailView(DetailView):
    queryset = Lead.objects.all()
    template_name = 'crmapp/leads/leads-detail.html'


class LeadDeleteView(UserPassesTestMixin, DeleteView):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.has_perm('crmapp.delete_lead')

    model = Lead
    form_class = ConfirmForm
    template_name = 'crmapp/leads/leads-delete.html'
    success_url = reverse_lazy('crmapp:leads')


class CustomersListView(ListView):
    queryset = Lead.objects.filter(is_active=True)
    template_name = 'crmapp/customers/customers-list.html'
    context_object_name = 'customers'
