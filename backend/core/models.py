from django.contrib.gis.db import models
from django.template.defaultfilters import slugify

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
	lon = models.FloatField(blank = True, null = True)
	lat = models.FloatField(blank = True, null = True)
	
	def __unicode__(self):
		if self.name:
			return "%s - %s" % (self.business_entity.name, self.name)
		else:
			return self.business_entity.name
