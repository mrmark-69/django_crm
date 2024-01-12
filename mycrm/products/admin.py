from django.contrib import admin

from products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = "id", "name", "description_short",
    list_display_links = "id", "name",
    ordering = "id", "name",
    search_fields = "name", "description", "id"
    fieldsets = [
        (None, {
            "fields": ("name", "description", "price"),
        }),
    ]

    def description_short(self, obj: Product) -> str:
        if len(obj.description) > 48:
            return f"{obj.description[:48]}..."
        return obj.description