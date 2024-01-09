from django.db import models
from django.urls import reverse


class Service(models.Model):
    class Meta:
        verbose_name = 'service'

    name = models.CharField(max_length=100, verbose_name="Name of service", db_index=True)
    description = models.CharField(max_length=500, null=False, blank=True, db_index=True)
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

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


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


class Customer(models.Model):
    lead = models.OneToOneField(Lead, on_delete=models.CASCADE, )
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, )

    def __str__(self) -> str:
        # noinspection PyUnresolvedReferences
        return f"{self.lead.last_name} {self.lead.first_name} {self.lead.phone}"
