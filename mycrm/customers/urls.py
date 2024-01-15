from django.urls import path

from customers import views

app_name = 'customers'

urlpatterns = [
    path("customers/", views.CustomersListView.as_view(), name="customers_list"),
    path("customers/new", views.CustomerCreateView.as_view(), name="add_customers"),
    path("customers/<int:pk>", views.CustomerDetailView.as_view(), name="customers_detail"),
    path("customers/<int:pk>/edit", views.CustomerUpdateView.as_view(), name="update_customer"),
    path("customers/<int:pk>/delete", views.CustomerDeleteView.as_view(), name="delete_customers"),
]
