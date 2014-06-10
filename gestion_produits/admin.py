# -*- coding: utf8 -*-
from django.contrib import admin

from easy_select2 import select2_modelform_meta
from gestion_produits.models import *


class ItemAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = (u'name', u'ref', u'quantity', u'stockage_modality',
            u'category', u'supplier', u'current_stock', )
    list_filter = (u'category', u'supplier',)
    search_fields = (u'name', u'category__name', u'supplier__name',)
    list_editable = (u'current_stock', )
    readonly_fields = (u'current_stock', )


class SupplierAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = (u'name', u'website', u'adress',)
    list_filter = (u'name', u'website', u'adress',)
    search_fields = (u'name', u'website', u'adress',)


admin.site.register(Category)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Item, ItemAdmin)
