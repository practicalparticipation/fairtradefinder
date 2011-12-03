from django.conf.urls.defaults import *
from piston.resource import Resource
from api.handlers import *

urlpatterns = patterns('',
	url(r'^(\w+)/location/(\d+)/', Resource(LocationHandler)),
	url(r'^(\w+)/locations/', Resource(LocationListHandler)),
	url(r'^(\w+)/product/(\d+)/', Resource(ProductHandler)),
	url(r'^(\w+)/products/', Resource(ProductListHandler)),
)
