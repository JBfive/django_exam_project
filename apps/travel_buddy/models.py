from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import datetime
import bcrypt

class UserManager(models.Manager):
	def basic_validator(self, postData):
		response = {
			'status': False,
			'errors': []
		}
		if len(postData['name']) < 3:
			response["errors"].append("Name should be at least 3 character")
		existing_users = User.objects.filter(username=postData['username'])
		if len(existing_users) > 0:
			response['errors'].append("Username already exists!")
		if len(postData['password']) < 8:
			response["errors"].append("Password must be longer than 8 characters")
		if len(postData['confirm']) < 8:
			response['errors'].append("Passwords must match at 8 or more characters")
		pwd=postData['password']
		cpwd=postData['confirm']
		if not cpwd == pwd:
			response['errors'].append("Passwords must match")
		if len(response['errors']) == 0:
			response['status'] = True
			response['user_id']= User.objects.create(
				name=postData['name'],
				username= postData['username'],
				password= bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
				).id
			print(response)
		return response
			
	def validate_login(self, postData):
		response = {
			'status': False,
			'errors': []
		}
		existing_user = User.objects.filter(username=postData['username'])
		if len(existing_user) == 0:
			print('errors')
			response['errors'].append('Invalid Login')
		else:
			if bcrypt.checkpw(postData['password'].encode(), existing_user[0].password.encode()):
				print("password match")
				response['status']=True
				response['user_id']=existing_user[0].id
			else:
				response['errors'].append("Failed to login")
		return response
	def validate_plan(self, postData):
		response = {
			'status': False,
			'errors': []
		}
		print(postData)
		if len(postData['destination']) < 1:
			response['errors'].append("Destination must be filled in")
		if len(postData['desc']) < 1:
			response['errors'].append("Description must be filled in")
		if len(postData['date_from']) < 1:
			response['errors'].append("Date must be filled in")
		if len(postData['date_to']) < 1:
			response['errors'].append("Date must be filled in")
		else:
			if len(response['errors']) == 0:
				response['status'] = True
				# print(user_id)
				# response['user_id'] = existing_user[0].id
				response['trip_id']= Trip.objects.create(
					destination=postData['destination'],
					desc= postData['desc'],
					date_from=postData['date_from'],
					date_to=postData['date_to']).id
			print(response)
		return response

class User(models.Model):
	name= models.CharField(max_length=255)
	username= models.CharField(max_length=255)
	password= models.CharField(max_length=255)
	created_at= models.DateTimeField(auto_now_add = True)
	updated_at= models.DateTimeField(auto_now = True)
	objects = UserManager()
	def __repr__(self):
		return "<User object: {} {}>".format(self.name, self.username)

class Trip(models.Model):
	destination=models.CharField(max_length=255)
	desc=models.TextField(max_length=1000)
	date_from=models.DateField()
	date_to=models.DateField()
	planner=models.ManyToManyField(User, related_name="planned")
	joiner=models.ManyToManyField(User, related_name="joined")
	created_at= models.DateTimeField(auto_now_add = True)
	updated_at= models.DateTimeField(auto_now = True)
	objects = UserManager()
	def __repr__(self):
		return "<Trip object: {} {}>".format(self.destination, self.desc, self.date_from, self.date_to, self.planner)