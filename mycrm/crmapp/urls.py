from django.contrib.auth.views import LoginView
from django.urls import path
from django.views.generic import TemplateView

from crmapp import views

app_name = 'crmapp'

urlpatterns = [
    path("accounts/logout/", views.logout_user, name="logout"),
    path("accounts/login/", views.login_user, name="login"),
    path("", TemplateView.as_view(template_name="crmapp/_base.html"), name='home'),
    path("users/statistic/", views.statistic, name='user_statistic')
]
