from django.db import models
from django.urls import reverse

from products.models import Product


class Advertisement(models.Model):
    campaign_name = models.TextField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    promotion_channel = models.CharField(max_length=255, null=False, blank=True)
    advertisement_budget = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'advertisement'

    def get_absolute_url(self):
        return reverse("ads:ads_detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return self.campaign_name
