from django.db import models

from products.models import Product


class Contract(models.Model):
    class Meta:
        verbose_name = 'contract'

    name = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    document = models.FileField(null=True, blank=True, upload_to="contracts_files/")
    date_signed = models.DateField()
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return self.name
