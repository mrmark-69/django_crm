from django.contrib.auth.views import LoginView
from django.urls import path
from django.views.generic import TemplateView

from crmapp import views

app_name = 'crmapp'

urlpatterns = [
    path("accounts/logout/", views.logout_user, name="logout"),
    path("accounts/login/", views.login_user, name="login"),
    path("", TemplateView.as_view(template_name="crmapp/_base.html"), name='home'),
    path("ads/", views.AdvertisingListView.as_view(), name="ads"),
    path("ads/new", views.AdvertisingCreateView.as_view(), name="ads_new"),
    path("ads/<int:pk>", views.AdvertisingDetailView.as_view(), name="ads_details"),
    path("ads/<int:pk>/edit", views.AdvertisingUpdateView.as_view(), name="update_ads"),
    path("ads/<int:pk>/delete", views.AdvertisingDeleteView.as_view(), name="delete_ads"),
    path("ads/statistic", views.StatisticListView.as_view(), name="ads_statistic"),
    path("products/", views.ServicesListView.as_view(), name="services_list"),
    path("products/<int:pk>", views.ServiceDetailView.as_view(), name="service_details"),
    path("products/<int:pk>/edit", views.ServiceUpdateView.as_view(), name="service_update"),
    path("products/new", views.ServiceCreateView.as_view(), name="add_service"),
    path("products/<int:pk>/delete", views.ServiceDeleteView.as_view(), name="delete_service"),
    path("contracts/", views.ContractsListView.as_view(), name="contracts"),
    path("contracts/new", views.ContractCreateView.as_view(), name="add_contract"),
    path("contracts/<int:pk>", views.ContractDetailView.as_view(), name="contracts_detail"),
    path("contracts/<int:pk>/delete/", views.ContractDeleteView.as_view(), name="delete_contract"),
    path("leads/", views.LeadsListView.as_view(), name="leads"),
    path("leads/new", views.LeadCreateView.as_view(), name="add_lead"),
    path("leads/<int:pk>/edit", views.LeadUpdateView.as_view(), name="edit_lead"),
    path("leads/<int:pk>", views.LeadDetailView.as_view(), name="leads_detail"),
    path("leads/<int:pk>/delete", views.LeadDeleteView.as_view(), name="delete_lead"),
    path("customers/", views.CustomersListView.as_view(), name="customers"),
    path("customers/new", views.CustomerCreateView.as_view(), name="add_customers"),
    path("customers/<int:pk>", views.CustomerDetailView.as_view(), name="customers_detail"),
    path("customers/<int:pk>/edit", views.CustomerUpdateView.as_view(), name="update_customer"),
    path("customers/<int:pk>/delete", views.CustomerDeleteView.as_view(), name="delete_customers"),
    path("users/statistic/", views.statistic, name='user_statistic')
]
