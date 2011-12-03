from django.contrib import admin
from core.models import BusinessEntity, Location, Locale, Product

class LocationInline(admin.TabularInline):
	model = Location

class ProductInline(admin.TabularInline):
	model = Product

admin.site.register(BusinessEntity, inlines=[LocationInline, ProductInline])
admin.site.register(Locale)
