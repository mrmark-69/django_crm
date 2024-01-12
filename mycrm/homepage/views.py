from django.shortcuts import render

from ads.models import Advertisement
from customers.models import Customer
from leads.models import Lead
from products.models import Product


def statistic(request):
    products_count = len(Product.objects.all())
    advertisements_count = len(Advertisement.objects.all())
    leads_count = len(Lead.objects.all())
    customers_count = len(Customer.objects.all())
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
