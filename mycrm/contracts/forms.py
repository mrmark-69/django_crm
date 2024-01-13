from django.forms import SelectDateWidget, ModelForm

from contracts.models import Contract


class ContractForm(ModelForm):
    class Meta:
        model = Contract
        fields = ('name', 'product', 'document', 'date_signed', 'start_date', 'end_date', 'amount')
        widgets = {
            'date_signed': SelectDateWidget(years=range(2024, 2034)),
            'start_date': SelectDateWidget(years=range(2024, 2034)),
            'end_date': SelectDateWidget(years=range(2024, 2034)),
        }