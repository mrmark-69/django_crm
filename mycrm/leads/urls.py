from django.urls import path

from leads import views

urlpatterns = [
    path("leads/", views.LeadsListView.as_view(), name="leads"),
    path("leads/new", views.LeadCreateView.as_view(), name="add_lead"),
    path("leads/<int:pk>/edit", views.LeadUpdateView.as_view(), name="edit_lead"),
    path("leads/<int:pk>", views.LeadDetailView.as_view(), name="leads_detail"),
    path("leads/<int:pk>/delete", views.LeadDeleteView.as_view(), name="delete_lead"),
]