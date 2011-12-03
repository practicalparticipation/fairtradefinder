from django.conf.urls.defaults import *
from piston.resource import Resource
from api.handlers import LocationHandler

location_handler = Resource(LocationHandler)

urlpatterns = patterns('',
	url(r'^(\w+)/location/(\d+)/', location_handler),
	url(r'^(\w+)/locations/', location_handler),
)
