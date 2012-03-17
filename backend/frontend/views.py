# Create your views here.
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from core.models import *

import collections

def homePage(request):

	return render_to_response('home.html')



def locationList(request):
	base = Location.objects.all()
	title = "Locations with Fairtrade products"

	if request.GET.get('business_id'):
		base = base.filter(business_entity__id = request.GET['business_id'])
	if request.GET.get('business_name'):
		base = base.filter(business_entity__name__istartswith = request.GET['business_name'])
	if request.GET.get('product_id'):
		base = base.filter(offerings__product__id = request.GET['product_id'])
		title = "Locations stocking " + Product.objects.filter(pk=request.GET['product_id'])[:1].get().name
	if request.GET.get('product_name'):
		base = base.filter(offerings__product__name__icontains = request.GET['product_name'])

	if request.GET.get('lat') and request.GET.get('lng'):
		my_location = Point(float(request.GET['lng']), float(request.GET['lat']))
		base = base.distance(my_location).order_by('distance')
		if request.GET.get('max_distance'):
			base = base.filter(point__distance_lte=(my_location, D(m=10000)))
		title = title + " nearby"	

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
	
	

	return render_to_response('location_listings.html', {'list': basePage,'title':title})
	

def locationView(request,location_id):
	location = get_object_or_404(Location,pk=location_id)

	products = {} #Creates a products dictionary
	for product in location.products.all(): #Loops through the available products
		try: #Try to append a value to our existing list
			products[product.category.name].append(product)
		except: #In the event a list doesn't already exist we need to create it
			products[product.category.name] = [product]

	return render_to_response('location_detail.html', {'location': location,'products': products})



def productList(request):
	base = Product.objects.all()
	
	products = {} #Creates a products dictionary
	for product in base: #Loops through the available products
		try: #Try to append a value to our existing list
			products[product.category.name].append(product)
		except: #In the event a list doesn't already exist we need to create it
			products[product.category.name] = [product]

	return render_to_response('product_listings.html', {'products': products})


def productView(request,product_id):
	product = get_object_or_404(Product,pk=product_id)

	lat = request.session.get('lat')
	lng = request.session.get('lng')

	locations = {} #Creates a products dictionary
	
	return render_to_response('product_detail.html', {'product': product,'locations': locations,'lat':lat,'lng':lng})


