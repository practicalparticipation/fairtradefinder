from piston.handler import BaseHandler
from core.models import Location, Locale, Product

class LocationHandler(BaseHandler):
	allowed_methods = ('GET',)
	model = Location
	fields = (
		'id', 'qualified_name', 'name', 'address', 'lon', 'lat',
		('business_entity', ('id','name'))
	)
	
	def read(self, request, locale_slug, location_id = None):
		locale = Locale.objects.get(slug=locale_slug)
		base = Location.objects.filter(locale=locale)
		
		if location_id:
			return base.get(pk=location_id)
		else:
			return base.all()

class ProductHandler(BaseHandler):
	allowed_methods = ('GET',)
	model = Product
	fields = (
		'id', 'name', 'description', 'url',
		('manufacturer', ('id','name'))
	)
	
	def read(self, request, locale_slug, product_id = None):
		locale = Locale.objects.get(slug=locale_slug)
		base = Product.objects.all()
		
		if product_id:
			return base.get(pk=product_id)
		else:
			return base.all()
