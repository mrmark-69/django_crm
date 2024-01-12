import logging

from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect

from ads.models import Advertisement
from customers.models import Customer
from leads.models import Lead
from products.models import Product

log = logging.getLogger(__name__)


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect("crmapp:home")
        else:
            return redirect('crmapp:login')
    else:
        return render(request, 'crmapp/registration/login.html')


def logout_user(request):
    logout(request)
    return redirect('crmapp:home')


# class LeadsListView(ListView):
#     template_name = 'crmapp/leads/leads-list.html'
#     context_object_name = 'leads'
#     queryset = (Lead.objects.all().select_related('campaign'))
#
#
# class LeadCreateView(UserPassesTestMixin, CreateView):
#     def test_func(self):
#         user = self.request.user
#         return user.is_superuser or user.has_perm('crmapp.add_lead')
#
#     model = Lead
#     fields = '__all__'
#     template_name = 'crmapp/leads/leads-create.html'
#     success_url = reverse_lazy('crmapp:leads')
#
#
# class LeadUpdateView(UserPassesTestMixin, UpdateView):
#     def test_func(self):
#         user = self.request.user
#         return user.is_superuser or user.has_perm('crmapp.change_lead')
#
#     model = Lead
#     fields = '__all__'
#     template_name = 'crmapp/leads/leads-edit.html'
#
#     def get_success_url(self):
#         return reverse(
#             'crmapp:leads_detail',
#             kwargs={'pk': self.object.pk}
#         )
#
#
# class LeadDetailView(DetailView):
#     queryset = Lead.objects.all()
#     template_name = 'crmapp/leads/leads-detail.html'
#
#
# class LeadDeleteView(UserPassesTestMixin, DeleteView):
#     def test_func(self):
#         user = self.request.user
#         return user.is_superuser or user.has_perm('crmapp.delete_lead')
#
#     model = Lead
#     form_class = ConfirmForm
#     template_name = 'crmapp/leads/leads-delete.html'
#     success_url = reverse_lazy('crmapp:leads')


def statistic(request):
    products_count = len(Product.objects.all())
    advertisements_count = len(Advertisement.objects.all())
    leads_count = len(Lead.objects.all())
    customers_count = len(Customer.objects.all())
    context = {
        'products_count': products_count,
        'advertisements_count': advertisements_count,
        'leads_count': leads_count,
        'customers_count': customers_count,
    }
    return render(
        request,
        'crmapp/users/index.html',
        context=context
    )
