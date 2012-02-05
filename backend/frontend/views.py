# Create your views here.
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from core.models import *

import collections

def locationList(request):
	base = Location.objects.all()

	if request.GET.get('lat') and request.GET.get('lng'):
			my_location = Point(float(request.GET['lng']), float(request.GET['lat']))
			base = base.distance(my_location).order_by('distance')
			if request.GET.get('max_distance'):
				base = base.filter(point__distance_lte=(my_location, D(m=request.GET['max_distance'])))

	paginator = Paginator(base, 20)

	page = request.GET.get('page',1)

	try:
	    basePage = paginator.page(page)
	except PageNotAnInteger:
	    # If page is not an integer, deliver first page.
	    basePage = paginator.page(1)
	except EmptyPage:
	    # If page is out of range (e.g. 9999), deliver last page of results.
	    basePage = paginator.page(paginator.num_pages)
	
	return render_to_response('location_listings.html', {'list': basePage})
	

def locationView(request,location_id):
	location = get_object_or_404(Location,pk=location_id)

	products = {} #Creates a products dictionary
	for product in location.products.all(): #Loops through the available products
		try: #Try to append a value to our existing list
			products[product.category.name].append(product)
		except: #In the event a list doesn't already exist we need to create it
			products[product.category.name] = [product]

	print products

	return render_to_response('location_detail.html', {'location': location,'products': products})