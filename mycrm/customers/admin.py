from django.contrib import admin

from customers.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = "id", "full_name", "contract",
    list_display_links = "id", "full_name", "contract",
    ordering = "id", "lead",
    search_fields = "lead", "contract", "id"
    fieldsets = [
        (None, {
            "fields": ("lead", "contract",),
        }),
    ]

    def full_name(self, obj: Customer) -> str:
        return f"{obj.lead.last_name} {obj.lead.first_name}"
