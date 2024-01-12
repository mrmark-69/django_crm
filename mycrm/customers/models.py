from django.db import models

from contracts.models import Contract
from leads.models import Lead


class Customer(models.Model):
    lead = models.OneToOneField(Lead, on_delete=models.CASCADE, )
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, )

    def __str__(self) -> str:
        # noinspection PyUnresolvedReferences
        return f"{self.lead.last_name} {self.lead.first_name} {self.lead.phone}"