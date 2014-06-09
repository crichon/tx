# -*- coding: utf8 -*-
from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

class Category(models.Model):
    name = models.CharField(u'categorie', max_length=50)

    class Meta:
        verbose_name = u'Catégorie'
        ordering = ["name"]

    def __unicode__(self):
        return self.name


class Supplier(models.Model):
    adress = models.CharField(u'adresse', max_length=50)
    name = models.CharField(u'nom', max_length=50)
    website = models.CharField(u'site web/catalogue', max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = u'Fournisseur'
        ordering = ["name"]

    def __unicode__(self):
        return self.name


class Item(models.Model):
    category = models.ForeignKey(Category, null=True, blank=True, verbose_name=u'Catégories')
    supplier = models.ForeignKey(Supplier, verbose_name=u'Fournisseur')
    ref = models.CharField(u'référence', max_length=50)
    name = models.CharField(u'identifiant', max_length=50)
    quantity = models.CharField(u'quantité par unité de vente', max_length=50)
    place = models.CharField(u'lieu de stockage', max_length=50)
    stockage_modality = models.CharField(u'modalité de stockage', max_length=50, null=True, blank=True)
    current_stock = models.IntegerField(verbose_name=u'Quantité en stock', default=0)

    class Meta:
        verbose_name = u'produit'
        ordering = ["name"]


    def __unicode__(self):
        return self.name  + u', ref: ' + self.ref + u' (' + self.category.name + u')'


class Order(models.Model):

    CURRENT = u'CU'
    DONE = u'D'
    CANCELED = u'CA'
    WAITING = u'W'
#    GET = u'G'

    ORDER_STATE = (
            (CURRENT, u'en cours'),
            (DONE, u'archivée'),
            (CANCELED, u'annulée'),
            (WAITING, u'en attente de réception'),
            #(GET, u'reçue'),
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

