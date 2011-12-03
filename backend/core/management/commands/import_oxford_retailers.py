from django.core.management.base import NoArgsCommand
from django.conf import settings
from core.models import Locale, BusinessEntity, Location, Product, ProductCategory, Offering
import csv, os

PATH = os.path.join(settings.ROOT_DIR, 'data/OxfordRetailers2011.csv')

class Command(NoArgsCommand):
	help = "Import the Oxford retailers data"
	def handle_noargs(self, *args, **kwargs):
		reader = csv.DictReader(open(PATH, 'rU'))
		
		oxford, created = Locale.objects.get_or_create(slug='oxford', defaults={'name': 'Oxford'})
		try:
			misc_category = ProductCategory.get_root_nodes().get(name='Miscellaneous')
		except ProductCategory.DoesNotExist:
			misc_category = ProductCategory.add_root(name='Miscellaneous')
		
		for row in reader:
			business, created = BusinessEntity.objects.get_or_create(name=row['Name of business'])
			location, created = Location.objects.get_or_create(
				locale=oxford,
				business_entity=business,
				name=row['Address'],
				defaults={'address': row['Address'], 'postcode': row['Postcode']}
			)
			
			location.offerings.all().delete()
			for product_key in row['Key'].split(';'):
				if product_key:
					product, created = Product.objects.get_or_create(
						fairtrade_org_uk_key=product_key,
						defaults={'name':product_key, 'category':misc_category}
					)
					Offering.objects.create(location=location, product=product)
