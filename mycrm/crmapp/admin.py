from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import path

from crmapp.models import Advertising, Service, Lead, Contract


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = "id", "name", "description_short",
    list_display_links = "id", "name",
    ordering = "id", "name",
    search_fields = "name", "description", "id"
    fieldsets = [
        (None, {
            "fields": ("name", "description", "price"),
        }),
    ]

    def description_short(self, obj: Service) -> str:
        if len(obj.description) > 48:
            return f"{obj.description[:48]}..."
        return obj.description


@admin.register(Advertising)
class AdvertisingAdmin(admin.ModelAdmin):
    list_display = "id", "advertising_campaign_name", "service", "promotion_channel",
    list_display_links = "id", "advertising_campaign_name",
    ordering = "id", "advertising_campaign_name",
    search_fields = "advertising_campaign_name", "service", "id"
    fieldsets = [
        (None, {
            "fields": ("advertising_campaign_name", "service", "promotion_channel", "advertising_budget"),
        }),
    ]


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = "id", "first_name", "phone", "email", "campaign",
    list_display_links = "id", "first_name", "phone",
    ordering = "id", "first_name",
    search_fields = "first_name", "phone", "id"
    fieldsets = [
        (None, {
            "fields": ("first_name", "last_name", "phone", "email", "campaign"),
        }),
    ]


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = "id", "name", "service", "document", "date_signed",
    list_display_links = "id", "name",
    ordering = "id", "name",
    search_fields = "name", "service", "id"
    fieldsets = [
        (None, {
            "fields": ("name", "service", "document", "date_signed", "start_date", "end_date", "amount"),
        }),
    ]
