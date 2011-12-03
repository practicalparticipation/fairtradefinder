from django.core.management.base import NoArgsCommand
from django.conf import settings
from core.models import Location
from time import sleep

class Command(NoArgsCommand):
	help = "Look up latitude/longitude for all locations that don't have them"
	def handle_noargs(self, *args, **kwargs):
		for location in Location.objects.filter(point__isnull = True):
			print "looking up %s" % location
			if location.geocode():
				location.save()
			sleep(2) # so we don't fall foul of Google rate limiting
