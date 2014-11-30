# -*- coding: utf8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect
from django import forms

from easy_select2 import select2_modelform_meta
from gestion_commandes.models import *
from gestion_produits.models import *
from datetime import datetime

import time
import xlwt

ORDER_CURRENT = (Order.ORDER_STATE[2], Order.ORDER_STATE[3])


def create_xls(obj):
    pass

def export_xls(ModelAdmin, request, queryset):
    """produce x file per order given in the queryset
    files are given "date_supplier.xls" name

    ugly and sub-optimise but well, their is deadline
    Also order won't be huge, so it's not a big deal !

    argh, don't know what's going on, should work, fucking lib
    """

    response = HttpResponse()

    #response[u'Content-Disposition'] = u'attachment; filename=commande_' + time.strftime("%d/%m/%Y") + u'.xls'
    f = open('/tmp/commande_' + time.strftime("%d-%m-%Y") + '.xls', 'w')
    wb = xlwt.Workbook(encoding='utf-8')

    suppliers = Supplier.objects.all()
    for order in queryset:
        for supp in suppliers:
            if order.items.filter(supplier__name=supp.name):

                ws = wb.add_sheet(supp.name)

                row_num = 0
                columns = (
                        (u"Identification", 12000),
                        (u"Référence", 5000),
                        (u"Quantité", 5000),
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
                    row_num += 1
                    row = (
                            #obj.item.category.name,
                            obj.item.name,
                            obj.item.ref,
                            obj.needed,
                            #obj.item.supplier.name,
                          )
                    for col_num in xrange(len(row)):
                        ws.write(row_num, col_num, row[col_num], font_style)
                wb.save(f)
    return response
export_xls.short_description = u"Export XLS"



class OrderFormCurrent(forms.ModelForm):
    def __init__(self,  *args, **kwargs):
        super(OrderFormCurrent, self).__init__(*args, **kwargs)
        self.fields[u'state'] = forms.ChoiceField(choices=ORDER_CURRENT)



class OrderAdmin(admin.ModelAdmin):
    list_per_page = 50
    actions = [export_xls]
    list_display = (u'create_date', u'state', u'order_date', u'completion_date', u'items_count')

    def get_actions(self, request):
        actions = super(OrderAdmin, self).get_actions(request)
        if not request.user.is_superuser:
            del actions[u'delete_selected']
        return actions


    def get_form(self, request, obj=None, **kwargs):
        """ Handle the choice given to the administator on the state's choices

        current -> *canceled or waiting
        waiting -> canceld

        other transition are handeld in self.save()
        *see below*
        except for done which is handeld by OrderItems.save() on state_change
        """
        self.readonly_fields = [u'create_date', u'order_date', u'completion_date']

        if not obj == None:
            if obj.state == Order.CURRENT:
                self.form = OrderFormCurrent
            else:
                self.readonly_fields.append(u'state')
        return super(OrderAdmin, self).get_form(request, obj, **kwargs)


    def save_model(self, request, obj, form, change):
        """ if state change to:
            - canceled, waiting -> create a new order
            - canceled -> mark OrderItems as canceled
            - waiting -> generate command
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
        obj.save()


class ItemForms(forms.ModelForm):

    Meta = select2_modelform_meta(OrderItems)

    def clean(self):
        """ add validation on form level, nicer for the user than an integrity error.
        Also, provide special user "tous" as a default value for "for_user" field.
        Done here as Django check constraint for each field provided with the form
        """
        order = Order.objects.get(state__startswith=Order.CURRENT)

        if not self.cleaned_data['for_user']:
            self.cleaned_data['for_user'] = User.objects.get(username__startswith=u'tous')

        if u'item' in self.cleaned_data and self.cleaned_data['item'] in order.items.all():
            msg = u'%s est déjà dans la facture courante, veuillez sélectionnez un autre produit' \
                    % self.cleaned_data['item']
            raise forms.ValidationError(msg)
        return self.cleaned_data


class OrderItemsAdmin(admin.ModelAdmin):
    """ Handles Items addition and actions"""

    form = ItemForms

    list_per_page = 50
    list_display = (u'my_item', 'item__quantity', u'item__supplier', u'needed', u'state', u'order_data', u'for_user')
    list_display_links = None

    search_fields = (u'for_user__username', u'item__name',)
    list_filter = (u'for_user', 'state', u'order_data', u'item__supplier')
    preserve_filters = True


    def my_item(self, instance):
        if instance.state == OrderItems.CURRENT:
            return u'<a href="./' + str(instance.id) + '" >' + instance.item.name + u'</a>'
        return instance.item.name
    my_item.allow_tags=True
    my_item.short_description = u'Commande'


    def item__quantity(self, instance):
        return instance.item.quantity
    item__quantity.short_description = u'Quantité par lot'


    def item__supplier(self, instance):
        return instance.item.supplier.name
    item__supplier.short_description = u'Fournisseur'


    def categories(self, instance):
        cat = [x.name for x in Category.objects.all()]
        return ",".join(cat)


    def changelist_view(self, request, extra_context = None):
        """ set current order as default filter
        todo, I should reverse url instead of harcoding it """
        test = request.META.get('HTTP_REFERER', u'').split(request.META['PATH_INFO'])

        if test[-1] and not test[-1].startswith(u'?'):
            if u'order_data__id__exact' not in request.GET:
                current_order_id = Order.objects.get(state__startswith=Order.CURRENT).id
                # Should use reverse url instead of hardcoding it
                return HttpResponseRedirect(u'/admin/gestion_commandes/orderitems/?order_data__id__exact=' + str(current_order_id))
        return super(OrderItemsAdmin, self).changelist_view(request, extra_context=extra_context)


    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        self.readonly_fields = []

        if obj == None:
            self.fieldsets = (
                (u'Produits', {
                    'fields': (u'categories', u'item', u'item__quantity', u'item__supplier')
                }),
                (u'Commmandes', {
                    'fields': (u'for_user', u'needed')
                }),
            );
            self.exclude.append(u'order_data')
            self.exclude.append(u'state')
            self.readonly_fields.append(u'categories')

        else:
            self.fieldsets = (
                (u'Champs éditables', {
                    'fields': (u'needed', u'for_user')
                }),
                (u'Informations', {
                    'fields': (u'order_data', u'item', u'item__quantity', u'item__supplier', u'state')
                }),
            );
            self.readonly_fields.append(u'order_data')
            self.readonly_fields.append(u'item')
            self.readonly_fields.append(u'state')

        self.readonly_fields.append(u'item__quantity')
        self.readonly_fields.append(u'item__supplier')
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
                self.message_user(request, \
                        u'%s est déjà dans la facture courante, veuillez plutôt l\'éditer' % obj.item, u'error')
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
            if obj.order_data.state == Order.WAITING and obj.state == OrderItems.GET:
                obj.state = OrderItems.DONE
                obj.save()
                i += 1
            else:
                self.message_user(request, u'%s n\'est pas dans les objets reçues' % obj.item, u'error')
        self.message_user(request, u'%d objet stockés' % i)


    def mark_as_missing(self, request, queryset):
        i = 0
        for obj in queryset:
            if obj.order_data.state == Order.WAITING and obj.state in (OrderItems.WAITING, OrderItems.CANCELED,):
                obj.state = OrderItems.MISSING
                obj.save()
                i += 1
            else:
                self.message_user(request, u'%s n\'est pas dans les objets en attente de réception' % obj.item, u'error')
        self.message_user(request, u'%d objet(s) manquant(s)' % i)


    def mark_as_canceled(self, request, queryset):
        i = 0
        for obj in queryset:
            if obj.order_data.state == Order.WAITING:
                obj.state = OrderItems.CANCELED
                obj.save()
                i += 1
                send_mail(u'Commande anulée',\
                        u'La commande de ' + obj.item.__unicode__() + u' a été anulée', request.user.email, \
                        [obj.for_user.email] if obj.for_user.username != u'tous' else\
                        [user.email for user in Group.objects.get(name__startswith=u'utilisateur').user_set.all()]\
                        , fail_silently=False
                )
            else:
                self.message_user(request, u'%s n\'est pas dans une commande non traitée' % obj.item, u'error')
        self.message_user(request, u'%d objet(s) annulée(s)' % i)


    def mark_as_get(self, request, queryset):
        i = 0
        for obj in queryset:
            if obj.order_data.state == Order.WAITING and obj.state in (OrderItems.WAITING, OrderItems.CANCELED,):
                obj.state = OrderItems.GET
                obj.save()
                i += 1
            else:
                self.message_user(request, u'%s n\'est pas en attente de réception' % obj.item, u'error')
        self.message_user(request, u'%d objet reçue(s)' % i)

    copy_items.short_description = u'copier vers la commande en cours'


    def get_actions(self, request):
        """ filter available actions depending on the user and the command state"""
        actions = super(OrderItemsAdmin, self).get_actions(request)

        pk = request.GET.get(u'order_data__id__exact', 0)
        if pk != 0:
            order = Order.objects.get(pk=pk)
            if order.state == Order.WAITING:
                pass
            else:
                del actions[u'mark_as_get']
                del actions[u'mark_as_stock']

            if u'responsables commandes' == request.user.groups.all()[0].name \
                and order.state == Order.WAITING:
                   return actions
        del actions['mark_as_canceled']
        del actions['mark_as_missing']
        return actions

    actions = [u'copy_items', u'mark_as_stock', u'mark_as_missing', u'mark_as_get', u'mark_as_canceled']
    copy_items.short_description = u'copier vers la commande en cours'
    mark_as_stock.short_description = u'marquer comme stockées'
    mark_as_missing.short_description = u'marquer comme manquants'
    mark_as_canceled.short_description = u'marquer comme annulées'
    mark_as_get.short_description = u'marquer comme reçues'


from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.core.urlresolvers import reverse


class LogEntryAdmin(admin.ModelAdmin):

    date_hierarchy = 'action_time'
    list_display_links = None

    def get_actions(self, request):
        actions = []
        return actions

    #readonly_fields = LogEntry._meta.get_all_field_names()

    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]


    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag',
        'change_message',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff and request.method != 'POST'

    def has_delete_permission(self, request, obj=None):
        return False

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = u'<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return link
    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = u'object'

    def queryset(self, request):
        return super(LogEntryAdmin, self).queryset(request) \
            .prefetch_related('content_type')


admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItems, OrderItemsAdmin)
