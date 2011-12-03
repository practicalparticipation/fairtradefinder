from django.contrib import admin
from core.models import BusinessEntity, Location

class LocationInline(admin.TabularInline):
	model = Location

admin.site.register(BusinessEntity, inlines=[LocationInline])
