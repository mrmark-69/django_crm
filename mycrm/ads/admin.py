from django.contrib import admin

from ads.models import Advertisement


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = "id", "campaign_name", "product", "promotion_channel"
    list_display_links = "id", "campaign_name",
    ordering = "id", "campaign_name",
    search_fields = "campaign_name", "product", "id"
    fieldsets = [
        (None, {
            "fields": ("campaign_name", "product", "promotion_channel", "advertisement_budget"),
        }),
    ]
