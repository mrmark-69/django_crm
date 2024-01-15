from django.db import models
from django.db.models import Manager, Q

from contracts.models import Contract
from leads.models import Lead


def get_available_contracts():
    used_contracts = Customer.objects.exclude(contract__isnull=True).values_list('contract', flat=True)
    return Q(pk__in=Contract.objects.exclude(pk__in=used_contracts))


class Customer(models.Model):
    objects = Manager()
    lead = models.OneToOneField(Lead, on_delete=models.CASCADE,
                                limit_choices_to=Q(customer__isnull=True))
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE,
                                    limit_choices_to=get_available_contracts)

    def __str__(self) -> str:
        # noinspection PyUnresolvedReferences
        return f"{self.lead.last_name} {self.lead.first_name} {self.lead.phone}"
