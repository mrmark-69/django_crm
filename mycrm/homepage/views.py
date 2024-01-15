from django.views.generic import ListView

from ads.models import Advertisement

from django.db.models import Count


class GeneralStatisticListView(ListView):
    model = Advertisement
    template_name = 'homepage/users/index.html'

    def get_queryset(self):
        queryset = Advertisement.objects.annotate(
            products_count=Count('product__price', distinct=True),
            advertisements_count=Count('pk', distinct=True),
            leads_count=Count('lead__pk', distinct=True),
            customers_count=Count('lead__customer', distinct=True),
        )
