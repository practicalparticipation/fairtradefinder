from piston.handler import BaseHandler
from core.models import Location, Locale, Product

class LocationListHandler(BaseHandler):
	allowed_methods = ('GET',)
	#model = Location
	fields = (
		'id', 'qualified_name', 'name', 'address', 'lon', 'lat',
		('business_entity', (
			'id', 'name',
		)),
	)
	
	def read(self, request, locale_slug):
		locale = Locale.objects.get(slug=locale_slug)
		base = Location.objects.filter(locale=locale)
		
		return base.all()

class LocationHandler(BaseHandler):
	allowed_methods = ('GET',)
	#model = Location
	fields = (
		'id', 'qualified_name', 'name', 'address', 'lon', 'lat',
		('business_entity', (
			'id','name',
		)),
		('products',(
			'id', 'name', 'qualified_name',
			('category', (
				'id', 'name',
			)),
			('manufacturer', (
				'id', 'name',
			))
		)),
	)
	
	def read(self, request, locale_slug, location_id):
		locale = Locale.objects.get(slug=locale_slug)
		base = Location.objects.filter(locale=locale)
		
		if location_id:
			return base.get(pk=location_id)
		else:
			return base.all()

class ProductListHandler(BaseHandler):
	allowed_methods = ('GET',)
	#model = Product
	fields = (
		'id', 'qualified_name', 'name',
		('category', (
			'id', 'name',
		)),
		('manufacturer', (
			'id','name'
		)),
	)
	
	def read(self, request, locale_slug):
		locale = Locale.objects.get(slug=locale_slug)
		base = Product.objects.filter(location__locale=locale)
		
		return base.distinct()

class ProductHandler(BaseHandler):
	allowed_methods = ('GET',)
	#model = Product
	fields = (
		'id', 'qualified_name', 'name', 'description', 'url',
		('category', (
			'id', 'name',
		)),
		('manufacturer', (
			'id','name'
		)),
		('locations',(
			'id', 'qualified_name', 'name', 'address', 'lon', 'lat',
			('business_entity', (
				'id', 'name',
			)),
		)),
	)
	
	def read(self, request, locale_slug, product_id):
		locale = Locale.objects.get(slug=locale_slug)
		base = Product.objects.all()
		
		if product_id:
			return base.get(pk=product_id)
		else:
			return base.all()
