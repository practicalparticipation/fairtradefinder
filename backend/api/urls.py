from django.conf.urls.defaults import *
from piston.resource import Resource
from api.handlers import *

location_handler = Resource(LocationHandler)
product_handler = Resource(ProductHandler)

urlpatterns = patterns('',
	url(r'^(\w+)/location/(\d+)/', location_handler),
	url(r'^(\w+)/locations/', location_handler),
	url(r'^(\w+)/product/(\d+)/', product_handler),
	url(r'^(\w+)/products/', product_handler),
)
