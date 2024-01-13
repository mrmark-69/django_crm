from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from homepage.forms import ConfirmForm
from leads.models import Lead


class LeadsListView(ListView):
    template_name = 'leads/leads-list.html'
    context_object_name = 'leads'
    queryset = (Lead.objects.select_related('campaign')).order_by('last_name')


class LeadCreateView(UserPassesTestMixin, CreateView):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.has_perm('leads.add_lead')

    model = Lead
    fields = '__all__'
    template_name = 'leads/leads-create.html'
    success_url = reverse_lazy('leads:leads')


class LeadUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.has_perm('leads.change_lead')

    model = Lead
    fields = '__all__'
    template_name = 'leads/leads-edit.html'

    def get_success_url(self):
        return reverse(
            'leads:leads_detail',
            kwargs={'pk': self.object.pk}
        )


class LeadDetailView(DetailView):
    queryset = Lead.objects.all()
    template_name = 'leads/leads-detail.html'


class LeadDeleteView(UserPassesTestMixin, DeleteView):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.has_perm('leads.delete_lead')

    model = Lead
    form_class = ConfirmForm
    template_name = 'leads/leads-delete.html'
    success_url = reverse_lazy('leads:leads')
