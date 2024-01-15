from django.db import models
from django.db.models import Manager

from ads.models import Advertisement


class Lead(models.Model):
    objects = Manager()

    class Meta:
        ordering = ['last_name']
        verbose_name = 'lead'

    first_name = models.CharField(max_length=25, null=True)
    last_name = models.CharField(max_length=25, null=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    campaign = models.ForeignKey(Advertisement, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name}"
