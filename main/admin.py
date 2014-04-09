# -*- coding: utf8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import admin
from django.shortcuts import redirect
from django.db import IntegrityError, transaction
from main.models import *


def create_xls(obj):
    pass


class OrderAdmin(admin.ModelAdmin):

    fields = (u'state', u'create_date', u'order_date', u'reception_date',)
    readonly_fields = (u'create_date', u'order_date', u'reception_date',)

    #def get_form(self, request, obj=None, **kwargs):
    #    """ override form or even disable admin right to change cmd by hand, use action """
    #    pass

    def save_model(self, request, obj, form, change):
        """ if state change to:
            - drop -> create a new order
            - backup -> create a new order
            - done -> create a new order, split items by supplier, generate pdf and send them via mail
        """
        print order_state[3][0]
        if change == True:
            if obj.state == order_state[2][0] or obj.state == order_state[3][0]:
                # save current order and create a new one
                new_order = Order()
                new_order.state = order_state[0][0]
                new_order.save()
                obj.save()
                if obj.state == order_state[3][0]:
                    # if order just been submitted, create xls
                    create_xls(obj)
            else:
                obj.save()
        else:
            obj.save()


from django import forms
class ItemForms(forms.ModelForm):
    class Meta:
        model=OrderItems

    def clean(self):
        order = Order.objects.get(state__startswith=u'en cours')
        if self.cleaned_data['item'] in order.items.all():
            msg = u'%s est déjà dans la facture courante, veuillez sélectionnez un autre produit' % self.cleaned_data['item']
            raise forms.ValidationError(msg)
        return self.cleaned_data


class OrderItemsAdmin(admin.ModelAdmin):

    form = ItemForms
    #fields = (u'order_data', u'item', u'needed', u'state', u'for_user',)
    # readonly_fields = (u'order_data',)
    actions = [u'copy_items', u'mark_as_stock', u'mark_as_missing']
    list_filter = (u'for_user', 'state', u'order_data')

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

        # Heu, just followed the docs on this one, but don\'t know wth this is
        self.exclude.append(u'user')
        return super(OrderItemsAdmin, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        """
        override save OrderItems

        - check if not already in the current order ?? (needed)
        - add for_user and user
        - if new, add it to the last order
        """
#        try:
#            current_order = Order.objects.get(state__startswith=u'en cours')
#        except ObjectDoesNotExist:
# init
#            current_order = Order()
#            current_order.state = order_state[0][0]
#            current_order.save()

        current_order = Order.objects.get(state__startswith=u'en cours')
        obj.user = request.user #
        if not obj.for_user:
            obj.for_user = request.user
        if change == False:
            obj.order_data = current_order
            obj.state = item_state[0][0]

#        if obj.item in current_order.items.all():
#            self.message_user(request, u'%s est déjà dans la facture courante, veuillez plutôt l\'éditer' % obj.item, u'error')
#            try:
#                with transaction.atomic():
#                    obj.save()
#            except IntegrityError:
#                redirect('/admin/main/orderitems') # ugly
#            print "fuck"
#        else:
#            print "fuckit"
        obj.save()
    # check if state change and if all orderItems are stocked -> archive order

    def copy_items(self, request, queryset):
        """ copy selected items to current order """
        current_order = Order.objects.get(state__startswith=u'en cours')
        i = 0
        for obj in queryset:
            if obj.order_data == current_order or obj.item in current_order.items.all():
                self.message_user(request, u'%s est déjà dans la facture courante, veuillez plutôt l\'éditer' % obj.item, u'error')
            else:
                item = OrderItems()
                item.state = item_state[0][0]
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
            if obj.order_data.state == u'archivée':
                obj.state=u'stocké'
                obj.save()
                i += 1
            else:
                self.message_user(request, u'%s n\'est pas dans une commande reçue' % obj.item, u'error')
        self.message_user(request, u'%d objet stockés' % i)


    def mark_as_missing(self, request, queryset):
        i = 0
        for obj in queryset:
            if obj.order_data.state == order_state[1][0]:
                obj.state = u'manquant'
                obj.save()
                i += 1
            else:
                self.message_user(request, u'%s n\'est pas dans une commande reçue' % obj.item, u'error')
        self.message_user(request, u'%d objet stockés' % i)

    copy_items.short_description = u'copier vers la facture en cours'
    mark_as_stock.short_description = u'marquer comme stockées'
    mark_as_missing.short_description = u'marquer comme manquants'

admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(Item)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItems, OrderItemsAdmin)
