from piston.handler import BaseHandler
from core.models import Location, Locale, Product, ProductCategory, LocationCategory

class LocationListHandler(BaseHandler):
	allowed_methods = ('GET',)
	#model = Location
	fields = (
		'id', 'qualified_name', 'name', 'address', 'lon', 'lat',
		('business_entity', (
			'id', 'name',
		)),
		('category', (
			'id', 'name',
		)),
	)
	
	def read(self, request, locale_slug):
		locale = Locale.objects.get(slug=locale_slug)
		base = Location.objects.filter(locale=locale)
		
		if request.GET.get('business_id'):
			base = base.filter(business_entity__id = request.GET['business_id'])
		if request.GET.get('business_name'):
			base = base.filter(business_entity__name__istartswith = request.GET['business_name'])
		if request.GET.get('product_id'):
			base = base.filter(offerings__product__id = request.GET['product_id'])
		if request.GET.get('product_name'):
			base = base.filter(offerings__product__name__icontains = request.GET['product_name'])
		
		if request.GET.get('product_category_id'):
			root_categories = ProductCategory.objects.filter(id = request.GET['product_category_id'])
			categories = []
			for root_category in root_categories:
				categories += [root_category] + list(root_category.get_descendants())
			print categories
			base = base.filter(offerings__product__category__in = categories)
		if request.GET.get('product_category_name'):
			root_categories = ProductCategory.objects.filter(name__icontains = request.GET['product_category_name'])
			categories = []
			for root_category in root_categories:
				categories += [root_category] + list(root_category.get_descendants())
			base = base.filter(offerings__product__category__in = categories)
		
		if request.GET.get('location_category_id'):
			root_categories = LocationCategory.objects.filter(id = request.GET['location_category_id'])
			categories = []
			for root_category in root_categories:
				categories += [root_category] + list(root_category.get_descendants())
			base = base.filter(category__in = categories)
		
		if request.GET.get('location_category_name'):
			root_categories = LocationCategory.objects.filter(name__icontains = request.GET['location_category_name'])
			categories = []
			for root_category in root_categories:
				categories += [root_category] + list(root_category.get_descendants())
			base = base.filter(category__in = categories)
		
		return base.distinct()

class LocationHandler(BaseHandler):
	allowed_methods = ('GET',)
	#model = Location
	fields = (
		'id', 'qualified_name', 'name', 'address', 'lon', 'lat',
		('business_entity', (
			'id','name',
		)),
		('category', (
			'id', 'name',
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
			('category', (
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
