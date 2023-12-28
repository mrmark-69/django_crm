from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Service(models.Model):
    class Meta:
        verbose_name = 'service'
        verbose_name_plural = "services"

    name = models.CharField(max_length=100, verbose_name="Name of service", db_index=True)
    description = models.CharField(max_length=200, null=False, blank=True)
    price = models.DecimalField(decimal_places=2)

    def __str__(self) -> str:
        return self.name


class Advertising(models.Model):
    advertising_campaign_name = models.TextField(null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    promotion_channel = models.CharField(max_length=255, null=False, blank=True)
    advertising_budget = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'advertising'

    def get_absolute_url(self):
        return reverse("crm_system:advertising_details", kwargs={"pk": self.pk})


class Lead(models.Model):
    class Meta:
        verbose_name = 'lead'

    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    campaign = models.ForeignKey(Advertising, on_delete=models.CASCADE)


class Contract(models.Model):
    class Meta:
        verbose_name = 'contract'

    name = models.CharField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
    document = models.FileField(upload_to="contracts/")
    date_signed = models.DateField()
    period = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
