from django.core.management.base import NoArgsCommand
from core.models import Product, BusinessEntity, ProductCategory
import urllib2
try:
	import simplejson as json
except ImportError:
	import json

URL = 'https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=json&name=fairtrade_products&query=select+*+from+`swdata`&apikey='

class Command(NoArgsCommand):
	help = "Import fairtrade.org.uk's list of products"
	def handle_noargs(self, *args, **kwargs):
		print "fetching product list"
		f = urllib2.urlopen(URL)
		products = json.loads(f.read())
		
		for (i, product_data) in enumerate(products):
			try:
				product = Product.objects.get(fairtrade_org_uk_key=product_data['key'])
			except Product.DoesNotExist:
				product = Product(fairtrade_org_uk_key=product_data['key'])
			
			manufacturer, created = BusinessEntity.objects.get_or_create(name=product_data['manufacturer'])
			
			category = None
			# walk down category tree
			for category_name in product_data['category'].split('/'):
				try:
					if not category:
						category = ProductCategory.get_root_nodes().get(name=category_name)
					else:
						category = category.get_children().get(name=category_name)
				except ProductCategory.DoesNotExist:
					raise Exception("Failed to locate category: %s" % product_data['category'])
			
			product.name = product_data['name']
			product.manufacturer = manufacturer
			product.category = category
			if product_data['description']:
				product.description = product_data['description']
			if product_data['url']:
				product.url = product_data['url']
			product.save()
			
			if i % 100 == 0:
				print "imported %d products" % i
