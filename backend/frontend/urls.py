from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url('locations/', 'frontend.views.locationList'),
	url('location/(?P<location_id>\d+)', 'frontend.views.locationView'),
)
