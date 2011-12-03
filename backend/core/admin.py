from django.contrib import admin
from core.models import BusinessEntity, Location, Locale

class LocationInline(admin.TabularInline):
	model = Location

admin.site.register(BusinessEntity, inlines=[LocationInline])
admin.site.register(Locale)
