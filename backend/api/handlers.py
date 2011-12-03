from piston.handler import BaseHandler
from core.models import Location, Locale

class LocationHandler(BaseHandler):
	allowed_methods = ('GET',)
	model = Location
	fields = (
		'id', 'qualified_name', 'name', 'address', 'lon', 'lat',
		('business_entity', ('id','name'))
	)
	
	def read(self, request, locale_slug, location_id = None):
		locale = Locale.objects.get(slug=locale_slug)
		base = Location.objects.filter(locale=locale)
		
		if location_id:
			return base.get(pk=location_id)
		else:
			return base.all()
