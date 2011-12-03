from django.contrib import admin
from treebeard.admin import TreeAdmin
from core.models import BusinessEntity, Location, Locale, Product, ProductCategory, Offering

class LocationInline(admin.TabularInline):
	model = Location

class ProductInline(admin.TabularInline):
	model = Product

class OfferingInline(admin.TabularInline):
	model = Offering
	raw_id_fields = ['product']

admin.site.register(BusinessEntity, inlines=[LocationInline, ProductInline])
admin.site.register(Locale)
admin.site.register(Product)
admin.site.register(ProductCategory, TreeAdmin)
admin.site.register(Location, inlines=[OfferingInline])
