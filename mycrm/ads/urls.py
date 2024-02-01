from django.urls import path

from ads import views

app_name = 'ads'

urlpatterns = [
    path("ads/", views.AdvertisementsListView.as_view(), name="ads"),
    path("ads/new", views.AdvertisementCreateView.as_view(), name="ads_new"),
    path("ads/<int:pk>", views.AdvertisementDetailsView.as_view(), name="ads_details"),
    path("ads/<int:pk>/edit", views.AdvertisementUpdateView.as_view(), name="update_ads"),
    path("ads/<int:pk>/delete", views.AdvertisementDeleteView.as_view(), name="delete_ads"),
    path("ads/statistic/", views.StatisticListView.as_view(), name="ads_statistic"),
]