from settings import *
from bundle_config import config

DATABASES['default'] = {
	'ENGINE': "django.contrib.gis.db.backends.postgis",
	'NAME': config['postgres']['database'],
	'USER': config['postgres']['username'],
	'PASSWORD': config['postgres']['password'],
	'HOST': config['postgres']['host'],
}
