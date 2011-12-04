from django.core.management.base import NoArgsCommand
from django.conf import settings
from core.models import *
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
			if not row['Name of business']:
				continue
			
			business, created = BusinessEntity.objects.get_or_create(name=row['Name of business'])
			
			if row['Notes']:
				business.notes = row['Notes']
			if row['Website']:
				business.website = row['Website']
			if row['Twitter']:
				business.twitter_name = row['Twitter']
			if row['Facebook']:
				business.facebook_name = row['Facebook']
			if row['YouTube']:
				business.youtube_name = row['YouTube']
			business.save()
			
			location_category = None
			for category_name in row['Type of business'].split('/'):
				if not location_category:
					try:
						location_category = LocationCategory.get_root_nodes().get(name=category_name)
					except LocationCategory.DoesNotExist:
						location_category = LocationCategory.add_root(name=category_name)
				else:
					try:
						location_category = location_category.get_children().get(name=category_name)
					except LocationCategory.DoesNotExist:
						location_category = location_category.add_child(name=category_name)
			
			try:
				location = Location.objects.get(
					locale=oxford,
					business_entity=business,
					name=row['Address'],
				)
				location.category = location_category
				location.address = row['Address']
				location.postcode = row['Postcode']
				location.save()
			except Location.DoesNotExist:
				location = Location.objects.create(
					locale=oxford,
					business_entity=business,
					name=row['Address'],
					address=row['Address'],
					postcode=row['Postcode'],
					category=location_category,
				)
			location.offerings.all().delete()
			for product_key in row['Key'].split(';'):
				if product_key:
					product, created = Product.objects.get_or_create(
						fairtrade_org_uk_key=product_key,
						defaults={'name':product_key, 'category':misc_category}
					)
					Offering.objects.create(location=location, product=product)
