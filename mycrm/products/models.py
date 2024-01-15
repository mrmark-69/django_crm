from django.db import models
from django.db.models import Manager


class Product(models.Model):
    objects = Manager()

    class Meta:
        verbose_name = 'product'

    name = models.CharField(max_length=100, verbose_name="Name of product", db_index=True)
    description = models.CharField(max_length=500, null=False, blank=True, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return self.name
