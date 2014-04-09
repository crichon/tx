# -*- coding: utf8 -*-
from django.contrib import admin
from main.models import *
import time
import pdb
from django.http import HttpResponse

def create_xls(obj):
    pass
def export_xls(ModelAdmin, request, queryset):
    import xlwt
    response = HttpResponse(mimetype='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=commande - '+time.strftime("%d/%m/%Y")+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    #For each categorie create sheet
    ws = wb.add_sheet("Commande")

    row_num = 0
    columns = [
            (u"Type de produit", 5000),
            (u"Identification", 12000),
            (u"Volume/Qté", 5000),
            (u"Référence", 5000),
            (u"Fournisseur", 5000),
            ]
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    #Set titles
    for col_num in xrange(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1

    for obj in queryset[0].order.order_by('supplier'):
        row_num += 1
        row = [
                obj.category.name,
                obj.name,
                obj.quantity,
                obj.ref,
                obj.supplier.name,
                ]
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response

export_xls.short_description = u"Export XLS"

class OrderAdmin(admin.ModelAdmin):
    actions = [export_xls]
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
