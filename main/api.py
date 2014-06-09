from tastypie.resources import ModelResource
from main.models import Item, Supplier, Category
from tastypie import fields


class SupplierResource(ModelResource):
    class Meta:
        queryset = Supplier.objects.all()
        resource_name = 'supplier'
        excludes=['id']
        include_resource_uri = False


#class CategoryResource(ModelResource):
    #class Meta:
        #queryset = Category.objects.all()
        #resource_name = 'category'
        #excludes=['id']
        #include_resource_uri = False


class ItemResource(ModelResource):
    #category = fields.ToOneField('main.api.CategoryResource', 'category', full = True)
    supplier = fields.ToOneField('main.api.SupplierResource', 'supplier', full = True)

    class Meta:
        queryset = Item.objects.all()
        resource_name = u'item'
        include_resource_uri = False

