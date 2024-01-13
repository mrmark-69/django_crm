from django.urls import path

from registration import views

app_name = 'registration'

urlpatterns = [
    path("accounts/logout/", views.logout_user, name="logout"),
    path("accounts/login/", views.login_user, name="login"),
]