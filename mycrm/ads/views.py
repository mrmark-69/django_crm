from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin
from django.db.models import Count, Sum, F, ExpressionWrapper, DecimalField
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from ads.forms import AdvertisementForm
from ads.models import Advertisement
from homepage.forms import ConfirmForm


class AdvertisementsListView(UserPassesTestMixin, ListView):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.has_perm('ads.view_advertisement')

    template_name = 'ads/ads-list.html'
    context_object_name = 'ads'
    queryset = Advertisement.objects.select_related('product').order_by('campaign_name')


class AdvertisementCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'ads.add_advertisement'

    model = Advertisement
    form_class = AdvertisementForm
    template_name = 'ads/ads-create.html'
    success_url = reverse_lazy('ads:ads')


class AdvertisementUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'ads.change_advertisement'

    model = Advertisement
    fields = '__all__'
    template_name = "ads/ads-edit.html"

    def get_success_url(self):
        return reverse(
            "ads:ads_details",
            kwargs={"pk": self.object.pk},
        )


class AdvertisementDetailsView(UserPassesTestMixin, DetailView):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.has_perm('ads.view_advertisement')

    queryset = Advertisement.objects.select_related('product')
    template_name = 'ads/ads-detail.html'


class AdvertisementDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'ads.delete_advertisement'

    model = Advertisement
    success_url = reverse_lazy("ads:ads")
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
            contracts_sum=Sum('lead__customer__contract__amount', distinct=True),
            # products_sum=Sum('product__price', distinct=True),
            profit=ExpressionWrapper(
                F('contracts_sum') / F('advertisement_budget'),
                output_field=DecimalField(),
            )
        ).order_by('campaign_name')

        return queryset
