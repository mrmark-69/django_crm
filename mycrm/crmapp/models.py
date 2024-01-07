from django.db import models
from django.urls import reverse


class Service(models.Model):
    class Meta:
        verbose_name = 'service'

    name = models.CharField(max_length=100, verbose_name="Name of service", db_index=True)
    description = models.CharField(max_length=200, null=False, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return self.name


class Advertising(models.Model):
    advertising_campaign_name = models.TextField(null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    promotion_channel = models.CharField(max_length=255, null=False, blank=True)
    advertising_budget = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'advertising'

    def get_absolute_url(self):
        return reverse("crmapp:ads_detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return self.advertising_campaign_name


class Lead(models.Model):
    class Meta:
        verbose_name = 'lead'

    first_name = models.CharField(max_length=25, null=True)
    last_name = models.CharField(max_length=25, null=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    campaign = models.ForeignKey(Advertising, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.full_name


class Contract(models.Model):
    class Meta:
        verbose_name = 'contract'

    name = models.CharField(max_length=255)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
    document = models.FileField(null=True, blank=True, upload_to="contracts/")
    date_signed = models.DateField()
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return self.name


# class Customers(models.Model):
#     first_name = models.ForeignKey(Lead, on_delete=models.CASCADE, null=True)
#     last_name = models.ForeignKey(Lead, on_delete=models.CASCADE, null=True, blank=True)
#     is_active = models.BooleanField(default=False)
