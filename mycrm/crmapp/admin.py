from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import path

from crmapp.models import Advertising, Service, Lead, Contract, Customer


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

    # def first_name(self, obj: Customer) -> str:
    #     return obj.lead.first_name
    #
    # def last_name(self, obj: Customer) -> str:
    #     return obj.lead.last_name

    def full_name(self, obj: Customer) -> str:
        return f"{obj.lead.last_name} {obj.lead.first_name}"



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
