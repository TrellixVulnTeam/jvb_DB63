import json
import datetime
import base64
import requests
import webbrowser
import pprint
from datetime import datetime, timedelta , date, timezone
import ast
import logging
import time
from pytz import timezone

from django.db.models import Q
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from rauth import OAuth2Service, OAuth2Session

from .models import FitbitConnectToken,\
					UserFitbitDataSleep,\
					UserFitbitDataHeartRate,\
					UserFitbitDataActivities,\
					UserFitbitDataSteps,\
					FitbitNotifications


def refresh_token_for_notification(user):
	'''
	This function updates the expired tokens in database
	Return: refresh token and access token
	'''
	client_id='22CN2D'
	client_secret='e83ed7f9b5c3d49c89d6bdd0b4671b2b'
	access_token_url='https://api.fitbit.com/oauth2/token'
	token = FitbitConnectToken.objects.get(user = user)
	refresh_token_acc = token.refresh_token
	client_id_secret = '{}:{}'.format(client_id,client_secret).encode()
	headers = {
		'Authorization':'Basic'+' '+base64.b64encode(client_id_secret).decode('utf-8'),
		'Content-Type':'application/x-www-form-urlencoded'
	}
	data = {
		'grant_type' : 'refresh_token',
		'refresh_token': refresh_token_acc,
	}
	request_data = requests.post(access_token_url,headers=headers,data=data)
	request_data_json = request_data.json()
	print(pprint.pprint(request_data_json))
	token_object = ''
	try: 
		token_object = FitbitConnectToken.objects.get(user=user)
		token_object.refresh_token=request_data_json['refresh_token'],
		token_object.access_token=request_data_json['access_token']
		token_object.save()
	except:
		logging.exception("message")
	if token_object:
		return (request_data_json['refresh_token'],request_data_json['access_token'])

def session_fitbit():
	'''
	return the session 
	'''
	service = OAuth2Service(
					 client_id='22CN2D',
					 client_secret='e83ed7f9b5c3d49c89d6bdd0b4671b2b',
					 access_token_url='https://api.fitbit.com/oauth2/token',
					 authorize_url='https://www.fitbit.com/oauth2/authorize',
					 base_url='https://fitbit.com/api')
	return service


def call_push_api(data):
	'''
		This function take the latest created_at from FitbitNotifications and get the data 
	'''
	print("Startes for checking notifications in database")

	# create_data = FitbitNotifications.objects.create(data_notification=data)
	# print(FitbitNotifications._meta.get_fields(),"fields")
	# updated_data = create_data.data_notification
	# updated_data = FitbitNotifications.objects.latest('created_at')
	if data:
		for i,k in enumerate(data):
			# k = ast.literal_eval(k)
			notification = k
			date = k['date']
			user_id = k['ownerId']
			data_type = k['collectionType']
			try:
				user = FitbitConnectToken.objects.get(user_id_fitbit=user_id).user
			except FitbitConnectToken.DoesNotExist as e:
				user = None
			if user:
				create_notification = FitbitNotifications.objects.create(user=user,collection_type=data_type,
					notification_date=date,state="unprocessed",notification= notification)
			service = session_fitbit()
			tokens = FitbitConnectToken.objects.get(user = user)
			access_token = tokens.access_token
			'''
		The updated_at will check the time when the access_token is (created or updated)
        As the access_token expires at every 8Hours. When celery job runs first we will check
        the access_token is not expries. If it expries we will update the access_token first then
        run the push notification job.
            '''
			token_updated_time = tokens.updated_at
			present_time = datetime.utcnow()
			datetime_obj_utc = present_time.replace(tzinfo=timezone('UTC'))
			check_token_expire = (datetime_obj_utc - token_updated_time).total_seconds()
			session = service.get_session(access_token)
			if check_token_expire < 28800:
				call_api(date,user_id,data_type,user,session,create_notification)
			else:
				session = get_session_and_access_token(user)
				call_api(date,user_id,data_type,user,session,create_notification)
	return None

def get_session_and_access_token(user):
	refresh_token,access_token = refresh_token_for_notification(user)
	service = session_fitbit()
	access_token = access_token
	session = service.get_session(access_token)	
	return session

def call_api(date,user_id,data_type,user,session,create_notification):
	'''
		This function call push notification messages and then store in to the 
		database

	Args: date(date which comes in push message)
		  user_id
		  data_type(type of data)
		  user(user instance)
		  session(created sesssion)
	Return: returns nothing
	'''
	
	# if data_type == 'body':
	# 	body_fat_fitbit = session.get(
	# 		"https://api.fitbit.com/1.2/user/{}/{}/log/fat/date/{}.json".format(
	# 		user_id,data_type,date))
	# 	body_fat_fitbit = body_fat_fitbit.json()
	# 	print(body_fat_fitbit, "testttttttttttt1")
	# 	body_weight_fitbit = session.get(
	# 		"https://api.fitbit.com/1/user/{}/body/log/weight/date/{}.json ".format(
	# 		user_id,date))
	# 	print(body_weight_fitbit, "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
	# 	body_weight_fitbit = body_weight_fitbit.json()
	# 	print(body_weight_fitbit, "testttttttttttt")

	if data_type == 'sleep':
		create_notification.state = "processing"
		create_notification.save()
		sleep_fitbit = session.get(
			"https://api.fitbit.com/1.2/user/{}/{}/date/{}.json".format(
			user_id,data_type,date))
		sleep_fitbit = sleep_fitbit.json()
		store_data(sleep_fitbit,user,date,create_notification,data_type='sleep_fitbit')
	elif data_type == 'activities':
		create_notification.state = "processing"
		create_notification.save()
		activity_fitbit = session.get(
		"https://api.fitbit.com/1/user/{}/activities/list.json?afterDate={}&sort=asc&limit=10&offset=0".format(
			user_id,date))
		heartrate_fitbit = session.get(
		"https://api.fitbit.com/1/user/{}/activities/heart/date/{}/1d.json".format(
			user_id,date))
		steps_fitbit = session.get(
		"https://api.fitbit.com/1/user/{}/activities/steps/date/{}/1d.json".format(
			user_id,date))
		if activity_fitbit:
			activity_fitbit = activity_fitbit.json()
			store_data(activity_fitbit,user,date,create_notification,data_type="activity_fitbit")
		if heartrate_fitbit:
			heartrate_fitbit = heartrate_fitbit.json()
			store_data(heartrate_fitbit,user,date,create_notification,data_type="heartrate_fitbit")
		if steps_fitbit:
			steps_fitbit = steps_fitbit.json()
			store_data(steps_fitbit,user,date,create_notification,data_type="steps_fitbit")
			# FitbitNotifications.objects.filter(user=user,
			# 	collection_type='Activities').update(state="processed")

	return None

def update_fitbit_data(user,date,create_notification,data,collection_type):
	'''
	This function updated the fitbit models 
	'''
	if collection_type == "activity_fitbit":
		UserFitbitDataActivities.objects.filter(user=user,
			date_of_activities=date).update(activities_data=data)
	elif collection_type == "sleep_fitbit":
		UserFitbitDataSleep.objects.filter(user=user,
			date_of_sleep=date).update(sleep_data=data)
	elif collection_type == "heartrate_fitbit":
		UserFitbitDataHeartRate.objects.filter(user=user,
			date_of_heartrate=date).update(heartrate_data=data)
	elif collection_type == "steps_fitbit":
		UserFitbitDataSteps.objects.filter(user=user,
			date_of_steps=date).update(steps_data=data)
    
	return None

def store_data(fitbit_all_data,user,start_date,create_notification,data_type=None):
	'''
	this function takes json data as parameter and store in database
	Args: fitbit_all_data should be in dict. If bulk data want to store, all data should be
		  inside dict 
		  user name,start data
	Return: None
	''' 
	start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
	if data_type:
		fitbit_all_data[data_type] = fitbit_all_data
	for key,value in fitbit_all_data.items():
		try:
			if "sleep_fitbit" == key:
				date_of_sleep = value['sleep'][0]['dateOfSleep']
				try:
					sleep_obj = UserFitbitDataSleep.objects.get(user=user,
					created_at=start_date)
					update_fitbit_data(user,date_of_sleep,create_notification,value,key)
					print("Updated sleep-Fitbit successfully")
					if create_notification != None:
						create_notification.state = "processed"
						create_notification.save()
				except UserFitbitDataSleep.DoesNotExist:
					UserFitbitDataSleep.objects.create(user=user,
					date_of_sleep=date_of_sleep,
					sleep_data=value,created_at=start_date)
					print("Created sleep-Fitbit successfully")
					if create_notification != None:
						create_notification.state = "processed"
						create_notification.save()
		except (KeyError, IndexError):
			logging.exception("message")
			if create_notification != None:
				create_notification.state = "failed"
				create_notification.save()

		try:
			if "activity_fitbit" == key:
				date_of_activity = value['pagination']['afterDate']
				try:
					activity_obj = UserFitbitDataActivities.objects.get(user=user,created_at=start_date)
					update_fitbit_data(user,date_of_activity,create_notification,value,key)
					print("Updated Activity-Fitbit successfully")
					if create_notification != None:
						create_notification.state = "processed"
						create_notification.save()
				except UserFitbitDataActivities.DoesNotExist:
					UserFitbitDataActivities.objects.create(user=user,
					date_of_activities=date_of_activity,
					activities_data=value,created_at=start_date)
					print("Created Activity-Fitbit successfully")
					if create_notification != None:
						create_notification.state = "processed"
						create_notification.save()

		except (KeyError, IndexError):
			logging.exception("message")
			if create_notification != None:
				create_notification.state = "failed"
				create_notification.save()

		try:
			if "heartrate_fitbit" == key:
				date_of_heartrate = value['activities-heart'][0]['dateTime']
				try:
					heartrate_obj = UserFitbitDataHeartRate.objects.get(user=user,
					created_at=start_date)
					update_fitbit_data(user,date_of_heartrate,create_notification,value,key)
					print("Updated Heartrate-Fitbit successfully")
				except UserFitbitDataHeartRate.DoesNotExist:
					UserFitbitDataHeartRate.objects.create(user=user,
					date_of_heartrate=date_of_heartrate,
					heartrate_data=value,created_at=start_date)
					print("Created heartrate-Fitbit successfully")
		except (KeyError, IndexError):
			logging.exception("message")


		try:
			if "steps_fitbit" == key:
				date_of_steps = value['activities-steps'][0]['dateTime']
				try:
					steps_obj = UserFitbitDataSteps.objects.get(user=user,
					created_at=start_date)
					update_fitbit_data(user,date_of_steps,create_notification,value,key)
					print("Updated steps-Fitbit successfully")
				except UserFitbitDataSteps.DoesNotExist:
					UserFitbitDataSteps.objects.create(user=user,
					date_of_steps=date_of_steps,
					steps_data=value,created_at=start_date)
					print("Created steps-Fitbit successfully")
		except (KeyError, IndexError):
			logging.exception("message")
	return None