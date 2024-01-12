from django import forms

from products.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", ]
        widgets = {
            'description': forms.Textarea(attrs={"cols": "40", "rows": "5"}),
        }
