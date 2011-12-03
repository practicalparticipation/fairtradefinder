from django.conf.urls.defaults import *
from piston.resource import Resource
from api.handlers import LocationHandler

location_handler = Resource(LocationHandler)

urlpatterns = patterns('',
	url(r'^location/(\d+)/', location_handler),
	url(r'^locations/', location_handler),
)
