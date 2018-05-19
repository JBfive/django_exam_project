from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import *


def index (request):
	return render(request, 'travel_buddy/index.html',{'user' : User.objects.all()})

def process (request):
	result = User.objects.basic_validator(request.POST)
	if result['status']== False:
		for error in result['errors']:
			messages.error(request, error)
		return redirect('/')
	else:
		request.session['user_id']= result['user_id']
		return redirect('/dashboard')
def login (request):
	result = User.objects.validate_login(request.POST)
	if result['status']== False:
		for error in result['errors']:
			messages.error(request, error)
		return redirect('/')
	else:
		request.session['user_id']= result['user_id']
		return redirect('/dashboard')

def dashboard(request):
	user=User.objects.get(id=request.session['user_id'])
	request.session['name']=user.name
	trip=Trip.objects.exclude(planner = request.session['user_id']).exclude(joiner = request.session['user_id'])
	my_plan= user.planned.all()
	joins= user.joined.all()

	context = {
		'trips': trip,
		'my_plan': my_plan,
		'joins': joins
	}

	return render(request, 'travel_buddy/dashboard.html', context)

def add_plan (request):
	return render(request, 'travel_buddy/add_plan.html')

def make_plan(request):
	result = Trip.objects.validate_plan(request.POST)
	if result['status'] == False:
		for error in result['errors']:
			messages.error(request, error)
		return redirect('/add_plan')
	else:
		# request.session['user_id']= result['user_id']
		request.session['trip_id']= result['trip_id']
		this_trip=Trip.objects.get(id=request.session['trip_id'])
		this_user=User.objects.get(id=request.session['user_id'])
		this_user.planned.add(this_trip)
		
	return redirect('/dashboard')

def destination (request, id):
	user=User.objects.get(id=request.session['user_id'])
	trip=Trip.objects.get(id=id)
	my_plan= trip.planner.all()
	joins= trip.joiner.exclude(id=request.session['user_id'])
	print(joins)
	context = {
		'trips': trip,
		'my_plan': my_plan,
		'joins': joins

	}

	return render(request, 'travel_buddy/destination.html', context)

def join (request, id):
	user=User.objects.get(id=request.session['user_id'])
	trip=Trip.objects.get(id=id)
	trip.joiner.add(request.session['user_id'])
	return redirect('/dashboard')


		# trip=Trip.objects.get(id=request.session['trip_id'])
		# this_trip=Trip.objects.get(id=request.session['trip_id'])
		# this_user=User.objects.get(id=request.session['user_id'])
	
	
		# context = {
		# 	'trip': Trip.objects.filter(id=trip.id),
		# 	'users': User.objects.exclude(id=user.id),
		# 	'plans': this_user.planned.all()
		# }

def clear (request):
	request.session.clear()
	return redirect('/') 