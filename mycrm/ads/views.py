from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Avg, Count, Min, Max, Sum, F, ExpressionWrapper, DecimalField
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from ads.forms import AdvertisementForm
from ads.models import Advertisement
from homepage.forms import ConfirmForm


class AdvertisementsListView(ListView):
    template_name = 'ads/ads-list.html'
    context_object_name = 'ads'
    queryset = Advertisement.objects.select_related('product').order_by('campaign_name')


class AdvertisementCreateView(UserPassesTestMixin, CreateView):
    def test_func(self):
        user = self.request.user
        return self.request.user.is_superuser or user.has_perm('ads.add_advertisement')

    model = Advertisement
    form_class = AdvertisementForm
    template_name = 'ads/ads-create.html'
    success_url = reverse_lazy('ads:ads')

    def form_valid(self, form):
        response = super().form_valid(form)
        form.instance.created_by = self.request.user

        return response


class AdvertisementUpdateView(UpdateView):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.has_perm('ads.change_advertisement')

    model = Advertisement
    fields = '__all__'
    template_name = "ads/ads-edit.html"

    def get_success_url(self):
        return reverse(
            "ads:ads_details",
            kwargs={"pk": self.object.pk},
        )


class AdvertisementDetailView(DetailView):
    queryset = Advertisement.objects.select_related('product')
    template_name = 'ads/ads-detail.html'


class AdvertisementDeleteView(UserPassesTestMixin, DeleteView):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.has_perm('ads.delete_advertisement')

    model = Advertisement
    success_url = reverse_lazy("homepage:ads")
    form_class = ConfirmForm
    template_name = "ads/ads-delete.html"


class StatisticListView(ListView):
    model = Advertisement
    template_name = 'ads/ads-statistic.html'
    context_object_name = 'ads'

    def get_queryset(self):
        queryset = Advertisement.objects.annotate(
            leads_count=Count('lead__pk', distinct=True),
            customers_count=Count('lead__customer', distinct=True),
            products_sum=Sum('product__price', distinct=True),
            profit=ExpressionWrapper(
                F('products_sum') / F('advertisement_budget'),
                output_field=DecimalField(),
            )
        ).order_by('campaign_name')

        return queryset
