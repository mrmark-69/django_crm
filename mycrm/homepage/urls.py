from django.urls import path
from django.views.generic import TemplateView

from homepage import views

app_name = 'homepage'

urlpatterns = [
    path("", TemplateView.as_view(template_name="homepage/_base.html"), name='home'),
    path("users/statistic/", views.general_statistic, name='user_statistic')
]
