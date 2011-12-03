from django.core.management.base import NoArgsCommand
from django.conf import settings
from core.models import ProductCategory
import csv, os

PATH = os.path.join(settings.ROOT_DIR, 'data/product_taxonomy.csv')

class Command(NoArgsCommand):
	help = "Import the product taxonomy file"
	def handle_noargs(self, *args, **kwargs):
		reader = csv.DictReader(open(PATH, 'rU'))
		for row in reader:
			try:
				parent = ProductCategory.get_root_nodes().get(name=row['Category'])
			except ProductCategory.DoesNotExist:
				parent = ProductCategory.add_root(name=row['Category'])
			
			try:
				child = parent.get_children().get(name=row['Product Type'])
			except ProductCategory.DoesNotExist:
				child = parent.add_child(name=row['Product Type'])
			
			if row['Description']:
				child.description = row['Description']
			if row['Link']:
				child.url = row['Link']
			child.save()
