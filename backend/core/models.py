from django.contrib.gis.db import models
from django.template.defaultfilters import slugify
from treebeard.mp_tree import MP_Node

class Locale(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField()
	
	def __unicode__(self):
		return self.name

class BusinessEntity(models.Model):
	name = models.CharField(max_length=255)
	
	def __unicode__(self):
		return self.name
	
	class Meta:
		verbose_name_plural = 'business entities'

class Location(models.Model):
	business_entity = models.ForeignKey(BusinessEntity, related_name = 'locations')
	locale = models.ForeignKey(Locale, related_name = 'locations')
	name = models.CharField(max_length=255, blank = True, null = True)
	address = models.TextField()
	postcode = models.CharField(max_length=16, blank=True, null=True)
	lon = models.FloatField(blank = True, null = True)
	lat = models.FloatField(blank = True, null = True)
	products = models.ManyToManyField('Product', through='Offering')
	
	@property
	def qualified_name(self):
		if self.name:
			return "%s - %s" % (self.business_entity.name, self.name)
		else:
			return self.business_entity.name
	
	def __unicode__(self):
		return self.qualified_name

class ProductCategory(MP_Node):
	name = models.CharField(max_length=255)
	description = models.TextField(blank=True, null=True)
	url = models.URLField(blank=True, null=True)
	
	node_order_by = ['name']
	
	def __unicode__(self):
		return self.name
	
	class Meta:
		verbose_name_plural = 'product categories'

class Product(models.Model):
	name = models.CharField(max_length=255)
	category = models.ForeignKey(ProductCategory, related_name='products')
	manufacturer = models.ForeignKey(BusinessEntity, related_name='products', blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	url = models.URLField(blank=True, null=True)
	fairtrade_org_uk_key = models.CharField(max_length=255, blank=True, null=True)
	locations = models.ManyToManyField('Location', through='Offering')
	
	@property
	def qualified_name(self):
		if self.manufacturer:
			return "%s %s" % (self.manufacturer.name, self.name)
		else:
			return self.name
	
	def __unicode__(self):
		return self.qualified_name

class Offering(models.Model):
	location = models.ForeignKey(Location, related_name='offerings')
	product = models.ForeignKey(Product, related_name='offerings')
	
	def __unicode__(self):
		return "%s at %s" % (self.product, self.location)
