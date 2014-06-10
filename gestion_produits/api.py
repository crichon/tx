from tastypie.resources import ModelResource
from gestion_produits.models import Item, Supplier, Category
from tastypie import fields


class SupplierResource(ModelResource):
    class Meta:
        queryset = Supplier.objects.all()
        resource_name = 'supplier'
        excludes=['id']
        include_resource_uri = False


class ItemResource(ModelResource):
    supplier = fields.ToOneField('gestion_produits.api.SupplierResource', 'supplier', full = True)

    class Meta:
        queryset = Item.objects.all()
        resource_name = u'item'
        include_resource_uri = False

