from django.contrib import admin
from .models import *


class UserModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "role", "email", "password", "contact"]


class SKUItemsModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "sku_name",
        "sku_qty",
        "sku_rate",
        "sku_serial_no",
        "sku_status",
        "sku_barcode_image",
    ]


class InvoiceModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "invoice_no",
        "invoice_party_name",
        "invoice_date",
        "invoice_item_scanned_status",
        "invoice_item_qty",
        "invoice_item_rate",
    ]


class ByPassModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "bypass_invoice_no",
        "bypass_sku_name",
        "bypass_against_sku_name",
        "bypass_date",
        "bypass_time",
    ]


admin.site.register(User, UserModelAdmin)
admin.site.register(SKUItems, SKUItemsModelAdmin)
admin.site.register(Invoice, InvoiceModelAdmin)
admin.site.register(ByPassModel, ByPassModelAdmin)
