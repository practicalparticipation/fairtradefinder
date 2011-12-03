from django.contrib import admin
from treebeard.admin import TreeAdmin
from core.models import BusinessEntity, Location, Locale, Product, ProductCategory

class LocationInline(admin.TabularInline):
	model = Location

class ProductInline(admin.TabularInline):
	model = Product

admin.site.register(BusinessEntity, inlines=[LocationInline, ProductInline])
admin.site.register(Locale)
admin.site.register(ProductCategory, TreeAdmin)
