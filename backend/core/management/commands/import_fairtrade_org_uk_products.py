from django.core.management.base import NoArgsCommand
from core.models import Product, BusinessEntity
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
			
			product.name = product_data['name']
			product.manufacturer = manufacturer
			if product_data['description']:
				product.description = product_data['description']
			if product_data['url']:
				product.url = product_data['url']
			product.save()
			
			if i % 100 == 0:
				print "imported %d products" % i
