from django.urls import path

from products import views

app_name = 'products'

urlpatterns = [
    path("products/", views.ProductsListView.as_view(), name="products_list"),
    path("products/<int:pk>", views.ProductDetailView.as_view(), name="product_details"),
    path("products/<int:pk>/edit", views.ProductUpdateView.as_view(), name="product_update"),
    path("products/new", views.ProductCreateView.as_view(), name="add_product"),
    path("products/<int:pk>/delete", views.ProductDeleteView.as_view(), name="delete_product"),
]
