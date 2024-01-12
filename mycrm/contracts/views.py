from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from contracts.models import Contract
from homepage.forms import ConfirmForm


class ContractsListView(ListView):
    template_name = 'contracts/contracts-list.html'
    context_object_name = 'contracts'
    queryset = (Contract.objects.all().select_related('product'))


class ContractCreateView(UserPassesTestMixin, CreateView):

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.has_perm('contracts.add_contract')

    model = Contract
    fields = '__all__'
    success_url = reverse_lazy("contracts:contracts_list")
    template_name = "contracts/contracts-create.html"


class ContractUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.has_perm('contracts.change_contract')

    model = Contract
    fields = '__all__'
    template_name = "contracts/contracts-edit.html"

    def get_success_url(self):
        return reverse(
            "contracts:contracts_detail",
            kwargs={"pk": self.object.pk},
        )


class ContractDetailView(DetailView):
    queryset = (Contract.objects.all().select_related('product'))
    template_name = "contracts/contracts-detail.html"


class ContractDeleteView(DeleteView):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.has_perm('contracts.delete_contract')

    model = Contract
    form_class = ConfirmForm
    success_url = reverse_lazy("contracts:contracts_list")
    template_name = "contracts/contracts-delete.html"

