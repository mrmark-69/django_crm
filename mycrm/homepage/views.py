from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from ads.models import Advertisement
from customers.models import Customer
from leads.models import Lead
from products.models import Product


def general_statistic(request: HttpRequest) -> HttpResponse:
    advertisements_count = Advertisement.objects.count()
    products_count = Product.objects.count()
    customers_count = Customer.objects.count()
    leads_count = Lead.objects.count()
    context = {
        'advertisements_count': advertisements_count,
        'products_count': products_count,
        'customers_count': customers_count,
        'leads_count': leads_count,
    }
    return render(request, 'homepage/users/index.html', context=context)
