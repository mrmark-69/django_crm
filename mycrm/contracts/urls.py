from django.urls import path

from contracts import views

app_name = 'contracts'

urlpatterns = [
    path("contracts/", views.ContractsListView.as_view(), name="contracts_list"),
    path("contracts/new", views.ContractCreateView.as_view(), name="add_contract"),
    path("contracts/<int:pk>", views.ContractDetailView.as_view(), name="contracts_detail"),
    path("contracts/<int:pk>/edit", views.ContractUpdateView.as_view(), name="edit_contract"),
    path("contracts/<int:pk>/delete/", views.ContractDeleteView.as_view(), name="delete_contract"),
]
