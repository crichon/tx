# -*- coding: utf8 -*-
from gestion_produits.models import Item
from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

import xlwt

class Order(models.Model):

    CURRENT = u'CU'
    DONE = u'D'
    CANCELED = u'CA'
    WAITING = u'W'

    ORDER_STATE = (
            (CURRENT, u'en cours'),
            (DONE, u'archivée'),
            (CANCELED, u'annulée'),
            (WAITING, u'en attente de réception'),
    )

    items = models.ManyToManyField(Item, through='OrderItems')
    state = models.CharField(u'état', max_length=50, choices=ORDER_STATE, default=CURRENT)
    create_date = models.DateField(u'date de création', auto_now_add=True)
    order_date = models.DateField(u'date d\'envoie', null=True, blank=True)
    completion_date = models.DateField(u'Date d\'archivage', null=True, blank=True)


    def items_count(self):
        return self.orderitems_set.count()
    items_count.short_description = u'Nombres d\'objets'


    def __unicode__(self):
        return 'commande du ' + self.create_date.strftime('%d/%m/%Y') + u', ' + self.get_state_display()

    class Meta:
        verbose_name = u'Validation des commande'


class OrderItems(models.Model):

    CURRENT = u'CU'
    DONE = u'D'
    CANCELED = u'CA'
    WAITING = u'W'
    GET = u'G'
    MISSING = u'M'

    ITEM_STATE = (
            (CURRENT, u'en attente de validation'),
            (WAITING, u'en attente de réception'),
            (GET, u'reçu, à stocker'),
            (DONE, u'stocké'),
            (MISSING, u'manquant'),
            (CANCELED, u'annulée'),
    )

    order_data = models.ForeignKey(Order, verbose_name=u'commande')
    item = models.ForeignKey(Item, verbose_name=u'objet')
    needed = models.IntegerField(verbose_name=u'quantité à commander', default=0)
    state = models.CharField(verbose_name=u'état', max_length=50, choices=ITEM_STATE)
    for_user = models.ForeignKey(User, related_name=u'OrderItems_for_user', verbose_name=u'pour', blank=True)
 # related name needed to help django manage multiple foreign keys on the same table
    user = models.ForeignKey(User, verbose_name=u'utilisateur')
    last_edited = models.DateField(u'date de création', auto_now=True)

    def __unicode__(self):
        return self.item.name + u', quantité: ' + str(self.needed) + u' ' + self.user.get_username() + u':' + self.get_state_display() + u' / ' + self.order_data.__unicode__()


    def save(self, *args, **kwargs):
        """ modify Order state depending on collections state
        if all items has been treated, mark order as done """
        super(OrderItems, self).save(*args, **kwargs)
        done = True
        if self.order_data.orderitems_set.all():
            for item in self.order_data.orderitems_set.all():
                if item.state not in (self.CANCELED, self.DONE, self.MISSING):
                    done = False
        else:
            done = False
        if done:
            self.order_data.completion_date = datetime.now()
            self.order_data.state = Order.DONE
            self.order_data.save()

        if self.state == self.DONE:
            self.item.current_stock += self.needed
            self.item.save()


    class Meta:
        verbose_name = u'Commande de produit'
        unique_together= (u'item', u'order_data',)

