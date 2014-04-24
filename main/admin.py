# -*- coding: utf8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import admin
from django.http import HttpResponse
from django import forms

from easy_select2 import select2_modelform_meta
from main.models import *
from datetime import datetime

import time
import xlwt

ORDER_CURRENT = (Order.ORDER_STATE[2], Order.ORDER_STATE[3])
ORDER_WAITING = (Order.ORDER_STATE[2], Order.ORDER_STATE[4])


def create_xls(obj):
    pass


def export_xls(ModelAdmin, request, queryset):
    """produce x file per order given in the queryset
    files are given "date_supplier.xls" name

    ugly and sub-optimise but well, their is deadline
    Also order won't be huge, so it's not aa big deal !

    argh, don't know what's going on, should work, fucking lib
    """

    response = HttpResponse(mimetype='application/ms-excel')
    response[u'Content-Disposition'] = u'attachment; filename=commande_' + time.strftime("%d/%m/%Y") + u'.xls'
    wb = xlwt.Workbook(encoding='utf-8')

    suppliers = Supplier.objects.all()
    #For each supplier create sheet
    for order in queryset:
        for supp in suppliers:
            print suppliers
            print supp.name
            if order.items.filter(supplier__name=supp.name):

                ws = wb.add_sheet(supp.name)

                row_num = 0
                columns = (
                        #(u"Type de produit", 5000),
                        (u"Identification", 12000),
                        #(u"Volume/Qté", 5000),
                        (u"Référence", 5000),
                        (u"Quantitée", 5000),
                        #(u"Fournisseur", 5000),
                        )
                font_style = xlwt.XFStyle()
                font_style.font.bold = True
                #Set titles
                for col_num in xrange(len(columns)):
                    ws.write(row_num, col_num, columns[col_num][0], font_style)
                    # set column width
                    ws.col(col_num).width = columns[col_num][1]

                font_style = xlwt.XFStyle()
                font_style.alignment.wrap = 1

                for obj in order.orderitems_set.filter(item__supplier__name=supp.name):
                    print obj
                    row_num += 1
                    row = (
                            #obj.item.category.name,
                            obj.item.name,
                            obj.item.ref,
                            obj.needed,
                            #obj.item.supplier.name,
                          )
                    print row
                    for col_num in xrange(len(row)):
                        ws.write(row_num, col_num, row[col_num], font_style)
                wb.save(response)
    return response
export_xls.short_description = u"Export XLS"


class OrderFormCurrent(forms.ModelForm):
    def __init__(self,  *args, **kwargs):
        super(OrderFormCurrent, self).__init__(*args, **kwargs)
        self.fields[u'state'] = forms.ChoiceField(choices=ORDER_CURRENT)


class OrderFormWaiting(forms.ModelForm):
    def __init__(self,  *args, **kwargs):
        super(OrderFormWaiting, self).__init__(*args, **kwargs)
        self.fields[u'state'] = forms.ChoiceField(choices=ORDER_WAITING)


class OrderAdmin(admin.ModelAdmin):
    actions = [export_xls]
    list_display = (u'create_date', u'state', u'order_date', u'reception_date', u'items_count')

    def get_form(self, request, obj=None, **kwargs):
        """ Handle the choice given to the administator on the state's choices

        current -> *canceled or waiting
        waiting -> canceld or *get

        other transition are handeld in self.save()
        *see below*
        except for done which is handeld by OrderItems.save() on state_change
        """
        # self.fields = [u'state', u'create_date', u'order_date', u'reception_date']
        self.readonly_fields = [u'create_date', u'order_date', u'reception_date']

        if not obj == None:
            if obj.state == Order.CURRENT:
                self.form = OrderFormCurrent
            elif obj.state == Order.WAITING:
                self.form = OrderFormWaiting
            else:
                self.readonly_fields.append(u'state')

        return super(OrderAdmin, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        """ if state change to:
            - canceled, waiting -> create a new order
            - canceled -> mark OrderItems as canceled
            - waiting -> generate command
            - get -> mark OrderItems as get
        """
        if change == True:
            if obj.state == Order.CANCELED or obj.state == Order.WAITING:
                # save current order and create a new one
                new_order = Order()
                new_order.state = Order.CURRENT
                new_order.save()
                if obj.state == Order.WAITING:
                    #order just been submitted
                    obj.order_date = datetime.now()
                    create_xls(obj)
                    for item in obj.orderitems_set.all():
                        item.state = OrderItems.WAITING
                        item.save()
                else:
                    # order is canceled
                    for item in obj.orderitems_set.all():
                        item.state = OrderItems.CANCELED
                        item.save()
            elif obj.state == Order.GET:
                obj.reception_date = datetime.now()
                for item in obj.orderitems_set.all():
                    item.state = OrderItems.GET
                    item.save()
        obj.save()


class ItemForms(forms.ModelForm):

    Meta = select2_modelform_meta(OrderItems)

    def clean(self):
        """ add validation on form level, nicer for the user than an integrity error"""

        # add validator for ro fields ???
        order = Order.objects.get(state__startswith=Order.CURRENT)
        if u'item' in self.cleaned_data and self.cleaned_data['item'] in order.items.all():
            msg = u'%s est déjà dans la facture courante, veuillez sélectionnez un autre produit' % self.cleaned_data['item']
            raise forms.ValidationError(msg)
        return self.cleaned_data


class OrderItemsAdmin(admin.ModelAdmin):
    """ Handles Items addition and actions
    user action, copy to current order
    items action, available when a command has arrived, mark as * """

    form = ItemForms
    actions = [u'copy_items', u'mark_as_stock', u'mark_as_missing', u'mark_as_canceled']
    list_display = (u'item', u'needed', u'state', u'order_data', u'for_user')
    search_fields = (u'for_user__username', u'item__name',)
    list_filter = (u'for_user', 'state', u'order_data')
    preserve_filters = True

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        self.readonly_fields = []
        if obj == None:
            self.exclude.append(u'order_data')
            self.exclude.append(u'state')
        else:
            self.readonly_fields.append(u'order_data')
            self.readonly_fields.append(u'item')
            self.readonly_fields.append(u'state')

        self.exclude.append(u'user')
        return super(OrderItemsAdmin, self).get_form(request, obj, **kwargs)

    def has_change_permission(self, request, obj=None):
        """ disable form depending on the object state"""
        if obj is not None and obj.order_data.state != Order.CURRENT:
            return False
        return super(OrderItemsAdmin, self).has_change_permission(request, obj)

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
            current_order = Order.objects.get(state__startswith=Order.CURRENT)
            obj.order_data = current_order
            obj.state = OrderItems.CURRENT
        obj.save()

    def copy_items(self, request, queryset):
        """ copy selected items to current order """
        current_order = Order.objects.get(state__startswith=Order.CURRENT)
        i = 0
        for obj in queryset:
            if obj.order_data == current_order or obj.item in current_order.items.all():
                self.message_user(request, u'%s est déjà dans la facture courante, veuillez plutôt l\'éditer' % obj.item, u'error')
            else:
                item = OrderItems()
                item.state = OrderItems.CURRENT
                item.needed = obj.needed
                item.for_user = obj.for_user
                item.user = request.user
                item.item = obj.item
                item.order_data = current_order
                item.save()
                i += 1
        self.message_user(request, u'%d objets ajouté(s)' %i)

    def mark_as_stock(self, request, queryset):
        i = 0
        for obj in queryset:
            if obj.order_data.state == OrderItems.GET:
                obj.state = OrderItems.DONE
                obj.save()
                i += 1
            else:
                self.message_user(request, u'%s n\'est pas dans une commande reçue' % obj.item, u'error')
        self.message_user(request, u'%d objet stockés' % i)


    def mark_as_missing(self, request, queryset):
        i = 0
        for obj in queryset:
            if obj.order_data.state == OrderItems.GET:
                obj.state = OrderItems.MISSING
                obj.save()
                i += 1
            else:
                self.message_user(request, u'%s n\'est pas dans une commande reçue' % obj.item, u'error')
        self.message_user(request, u'%d objet stockés' % i)


    def mark_as_canceled(self, request, queryset):
        i = 0
        for obj in queryset:
            if obj.order_data.state == OrderItems.GET:
                obj.state = OrderItems.MISSING
                obj.save()
                i += 1
            else:
                self.message_user(request, u'%s n\'est pas dans une commande reçue' % obj.item, u'error')
        self.message_user(request, u'%d objet annulée(s)' % i)

    copy_items.short_description = u'copier vers la facture en cours'
    mark_as_stock.short_description = u'marquer comme stockées'
    mark_as_missing.short_description = u'marquer comme manquants'
    mark_as_canceled.short_description = u'marquer comme annulées'


class ItemAdmin(admin.ModelAdmin):
    list_display = (u'name', u'quantity', u'stockage_modality', u'category', u'supplier',)
    list_filter = (u'category__name', u'supplier__name',)
    search_fields = (u'name', u'category__name', u'supplier__name',)


class SupplierAdmin(admin.ModelAdmin):
    list_display = (u'name', u'website', u'adress',)
    list_filter = (u'name', u'website', u'adress',)
    search_fields = (u'name', u'website', u'adress',)


admin.site.register(Category)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItems, OrderItemsAdmin)
