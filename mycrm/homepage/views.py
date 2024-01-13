from django.shortcuts import render

from ads.models import Advertisement
from customers.models import Customer
from leads.models import Lead
from products.models import Product


def statistic(request):
    products_count = Product.objects.count()
    advertisements_count = Advertisement.objects.count()
    leads_count = Lead.objects.count()
    customers_count = Customer.objects.count()
    context = {
        'products_count': products_count,
        'advertisements_count': advertisements_count,
        'leads_count': leads_count,
        'customers_count': customers_count,
    }
    return render(
        request,
        'homepage/users/index.html',
        context=context
    )
