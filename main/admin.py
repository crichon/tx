# -*- coding: utf8 -*-
from django.contrib import admin
from main.models import *


def create_xls(obj):
    pass


class OrderAdmin(admin.ModelAdmin):

    fields = (u'state', u'create_date', u'order_date', u'reception_date',)
    readonly_fields = (u'create_date', u'order_date', u'reception_date',)

    def save_model(self, request, obj, form, change):
        """ if state change to:
            - drop -> create a new order
            - backup -> create a new order
            - done -> create a new order, split items by supplier, generate pdf and send them via mail
        """
        if change == True:
            if obj.state == order_state[2][0] or order_date[3][0]:
                # save current order and create a new one
                new_order = Order()
                new_order.save()
                obj.save()
                if obj.state == order[3][0]:
                    # if order just been submitted, create xls
                    create_xls(obj)
        else:
            obj.save()


class OrderItemsAdmin(admin.ModelAdmin):

    fields = (u'order_data', u'item', u'needed', u'state', u'for_user',)
    readonly_fields = (u'order_data',)

    def save_model(self, request, obj, form, change):
        """add for_user and user to item orderring"""
        obj.user = request.user
        if not obj.user:
            obj.for_user = request.user
        obj.save()


admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(Item)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItems, OrderItemsAdmin)
