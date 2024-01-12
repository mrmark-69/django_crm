from django.contrib import admin

from contracts.models import Contract


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = "id", "name", "product", "document", "date_signed",
    list_display_links = "id", "name",
    ordering = "id", "name",
    search_fields = "name", "product", "id"
    fieldsets = [
        (None, {
            "fields": ("name", "product", "document", "date_signed", "start_date", "end_date", "amount"),
        }),
    ]
