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

    #fields = (u'order_data', u'item', u'needed', u'state', u'for_user',)
    # readonly_fields = (u'order_data',)

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        self.readonly_fields = []
        if obj == None:
            self.exclude.append(u'order_data')
            self.exclude.append(u'state')
        else:
            self.readonly_fields.append(u'order_data')
            self.readonly_fields.append(u'state')
        # Heu, just followed the docs on this one, but don\'t know wth this is
        self.exclude.append(u'user')
        return super(OrderItemsAdmin, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        """
        override save OrderItems

        - add for_user and user
        - if new, add it to the last order
        """
        obj.user = request.user
        if not obj.for_user:
            obj.for_user = request.user

        if change == False:
            obj.order_data = Order.objects.get(state__startswith=u'en cours')
        obj.save()
    # check if state change and if all orderItems are stocked -> archive order


admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(Item)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItems, OrderItemsAdmin)
