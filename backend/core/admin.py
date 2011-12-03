from django.contrib.gis import admin
from treebeard.admin import TreeAdmin
from core.models import *

class LocationInline(admin.TabularInline):
	model = Location
	exclude = ['point']

class ProductInline(admin.TabularInline):
	model = Product

class OfferingInline(admin.TabularInline):
	model = Offering
	raw_id_fields = ['product']

admin.site.register(BusinessEntity, inlines=[LocationInline, ProductInline])
admin.site.register(Locale)
admin.site.register(Product, list_display = ['name', 'manufacturer', 'category'])
admin.site.register(ProductCategory, TreeAdmin)
admin.site.register(LocationCategory, TreeAdmin)
admin.site.register(Location, admin.OSMGeoAdmin, inlines=[OfferingInline])
