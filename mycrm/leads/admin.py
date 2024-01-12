from django.contrib import admin

from leads.models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = "id", "full_name", "phone", "email", "campaign",
    list_display_links = "id", "full_name", "phone",
    ordering = "id", "first_name",
    search_fields = "first_name", "phone", "id"
    fieldsets = [
        (None, {
            "fields": ("first_name", "last_name", "phone", "email", "campaign"),
        }),
    ]

    def full_name(self, obj: Lead) -> str:
        return f"{obj.last_name} {obj.first_name}"