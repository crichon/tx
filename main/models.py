# -*- coding: utf8 -*-
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField('categorie', max_length=50)

    class Meta:
        verbose_name = u'Catégorie'

    def __unicode__(self):
        return self.name


class Supplier(models.Model):
    adress = models.CharField(u'adresse', max_length=50)
    name = models.CharField(u'nom', max_length=50)
    website = models.CharField(u'site web/catalogue', max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = u'Fournisseur'

    def __unicode__(self):
        return self.name


class Item(models.Model):
    category = models.ForeignKey(Category, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, null=True, blank=True)
    ref = models.CharField(u"référence", max_length=50)
    name = models.CharField(u'identifiant', max_length=50)
    quantity = models.CharField(u'quantité/volume', max_length=50)
    place = models.CharField(u'lieu de stockage', max_length=50)
    stockage_modality = models.CharField(u'modalité de stockage', max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = u'produit'


    def __unicode__(self):
        return self.name


order_state = (
        (u'en cours', u'en cours'),
        (u'archivée', u'archivée'),
        (u'anulée', u'annulée'),
        (u'en attente', u'en attente de réception'),
)

class Order(models.Model):
    items = models.ManyToManyField(Item, through='OrderItems')
    state = models.CharField(u'état', max_length=50, choices=order_state, default=order_state[0])
    create_date = models.DateField(u'date de création', auto_now_add=True)
    order_date = models.DateField(u'date d\'envoie de la commande', null=True, blank=True)
    reception_date = models.DateField(u'Date de réception de la commande', null=True, blank=True)

    def __unicode__(self):
        return 'commande du ' + self.create_date.strftime('%d/%m/%Y') + u', ' + self.state

    class Meta:
        verbose_name = u'Commande'


item_state = (
        (u'en attente de validation', u'en attente de validation'),
        (u'anulée', u'annulée'),
        (u'stocké', u'stocké'),
        (u'en attente de réception', u'en attente de réception'),
)


class OrderItems(models.Model):
    order_data = models.ForeignKey(Order, verbose_name=u'commande')
    item = models.ForeignKey(Item, verbose_name=u'objet')
    needed = models.IntegerField(verbose_name=u'quantité à commander', default=0)
    state = models.CharField(verbose_name=u'état', max_length=50, choices=item_state)
    for_user = models.ForeignKey(User, related_name=u'OrderItems_for_user', verbose_name=u'pour', blank=True, null=True) # related name needed to help django manage multiple foreign keys on the same table
    user = models.ForeignKey(User, verbose_name=u'utilisateur')
    last_edited = models.DateField(u'date de création', auto_now=True)

    def __unicode__(self):
        return self.item.name + u', quantité: ' + str(self.needed) + u' ' + self.user.get_username() + u'/ ' + self.order_data.__unicode__()

    class Meta:
        verbose_name = u'Commande de produit'

