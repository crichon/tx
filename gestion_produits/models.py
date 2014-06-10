# -*- coding: utf8 -*-
from django.db import models


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

