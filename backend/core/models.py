from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.dispatch import receiver
from treebeard.mp_tree import MP_Node
from time import sleep
import urllib
try:
	import simplejson as json
except ImportError:
	import json

class Locale(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField()
	
	def __unicode__(self):
		return self.name

class BusinessEntity(models.Model):
	name = models.CharField(max_length=255)
	notes = models.TextField(blank=True, null=True)
	website = models.URLField(blank=True, null=True)
	twitter_name = models.CharField(max_length=50, blank=True, null=True)
	facebook_name = models.CharField(max_length=50, blank=True, null=True)
	youtube_name = models.CharField(max_length=50, blank=True, null=True)
	
	def __unicode__(self):
		return self.name
	
	class Meta:
		verbose_name_plural = 'business entities'

class LocationCategory(MP_Node):
	name = models.CharField(max_length=255)
	
	node_order_by = ['name']
	
	def __unicode__(self):
		return self.name
	
	class Meta:
		verbose_name_plural = 'location categories'

class Location(models.Model):
	business_entity = models.ForeignKey(BusinessEntity, related_name = 'locations')
	locale = models.ForeignKey(Locale, related_name = 'locations')
	name = models.CharField(max_length=255, blank = True, null = True)
	category = models.ForeignKey(LocationCategory, related_name='locations')
	address = models.TextField()
	postcode = models.CharField(max_length=16, blank=True, null=True)
	point = models.PointField(blank=True, null=True,srid=27700)
	products = models.ManyToManyField('Product', through='Offering')
	
	objects = models.GeoManager()
	
	def save(self, *args, **kwargs):
		self.geocode()
		super(Location, self).save()

	def geocode(self):
		if(self.postcode):
			address = "%s, UK" % (self.postcode)
		else:	
			address = "%s, %s, %s, UK" % (self.address, self.locale.name, self.postcode)
		lookup_url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % urllib.quote(address.encode("utf-8"))
		print lookup_url
		f = urllib.urlopen(lookup_url)
		response = json.loads(f.read())
		if len(response['results']):
			lat_lng = response['results'][0]['geometry']['location']
			self.point = Point(lat_lng['lng'], lat_lng['lat'])
		return self.point
	
	@property
	def qualified_name(self):
		if self.name:
			return "%s - %s" % (self.business_entity.name, self.name)
		else:
			return self.business_entity.name
	
	@property
	def lng(self):
		if self.point:
			return self.point.x
	@property
	def lat(self):
		if self.point:
			return self.point.y
	@property
	def distance_metres(self):
		if self.distance:
			return self.distance.m
	
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



    
