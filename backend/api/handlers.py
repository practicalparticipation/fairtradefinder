from piston.handler import BaseHandler
from core.models import Location

class LocationHandler(BaseHandler):
	allowed_methods = ('GET',)
	model = Location
	
	def read(self, request, location_id = None):
		base = Location.objects
		
		if location_id:
			return base.get(pk=location_id)
		else:
			return base.all()
