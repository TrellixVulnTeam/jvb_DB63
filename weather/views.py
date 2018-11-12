import ast
import json
import requests
import time
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from user_input.models import DailyActivity
from garmin.models import UserGarminDataActivity
from user_input.views.garmin_views import _get_activities_data
from quicklook.calculations.garmin_calculation import get_filtered_activity_stats
from user_input.utils.daily_activity import get_daily_activities_in_base_format

class ActivityWeatherView(APIView):

    def get(self, request):
        user = self.request.user
        start_dt = self.request.query_params.get('start_date',None)
        weather_report = self.get_weather_info_for_filtered_activities(user, start_dt)
        return weather_report

    def get_weather_info_for_filtered_activities(self, user, date):
        activities = get_daily_activities_in_base_format(user, date)
        garmin_list, manually_edited_list = _get_activities_data(user, date)
        manually_edited = {dic['summaryId']:dic for dic in manually_edited_list}

        filtered_activities_list = get_filtered_activity_stats(activities_json=garmin_list,
                            manually_updated_json=manually_edited,
                            userinput_activities=activities)
        weather_data = {}
        for activity in filtered_activities_list:
            epoch_time = activity['startTimeInSeconds']+activity['startTimeOffsetInSeconds']
            if activity.get('activity_weather') == {}:
                if 'startingLatitudeInDegree' in activity:
                    latitude = activity['startingLatitudeInDegree']
                    longitude = activity['startingLongitudeInDegree']

                    activity_weather = get_weather_response_as_required(
                                            latitude, longitude, epoch_time)

                    weather_data[activity['summaryId']] = {**activity_weather}
                else:
                    weather_report = get_weather_info_using_garmin_activity(
                                                user, epoch_time, activity['summaryId'])
                    weather_data[activity['summaryId']] = {**weather_report}
            else:
                weather_report = get_weather_info_using_garmin_activity(
                                                user, epoch_time, activity['summaryId'])
                weather_data[activity['summaryId']] = {**weather_report}
        return Response(weather_data)


def get_weather_info_using_garmin_activity(user, epoch_time, summaryId):
    weather_report = {'dewPoint': {'value': None, 'units': None},
                                'humidity': {'value': None, 'units': None},
                                'temperature':{'value': None, 'units': None},
                                'wind': {'value': None, 'units': None},
                                'temperature_feels_like':{'value': None, 'units': None},
                                'weather_condition': None}
    try:
        garmin_activity = UserGarminDataActivity.objects.get(user=user, summary_id=summaryId)
        garmin_activity_data = ast.literal_eval(garmin_activity.data)
        if 'startingLatitudeInDegree' in garmin_activity_data:
            latitude = garmin_activity_data['startingLatitudeInDegree']
            longitude = garmin_activity_data['startingLongitudeInDegree']

            activity_weather = get_weather_response_as_required(
                                    latitude, longitude, epoch_time)
            weather_report.update({**activity_weather})
        return weather_report
    except UserGarminDataActivity.DoesNotExist:
        return weather_report


def get_weather_response_as_required(latitude, longitude, epoch_time):
    weather_info = get_weather_info_using_lat_lng_time(latitude, longitude, epoch_time)

    # dewPoint_value = round((weather_info['currently']['dewPoint'] * 9/5)+ 32, 2)
    # temperature_value = round((weather_info['currently']['temperature'] * 9/5)+ 32, 2)
    # temperature_feels_like_value = round((weather_info['currently']['apparentTemperature'] * 9/5)+ 32, 2)
    humidity_value = weather_info['currently']['humidity']*100
    wind_value = round(weather_info['currently']['windSpeed']*2.237, 2)
                    
    activity_weather = {'dewPoint': {'value': weather_info['currently']['dewPoint'], 'units': 'celsius'},
                                            # 'value': dewPoint_value, 'units': 'fahrenheit'},
                'humidity': {'value': humidity_value, 'units': 'percentage'},
                'temperature':{'value': weather_info['currently']['temperature'], 'units': 'celsius'},
                                # 'value': temperature_value, 'units': 'fahrenheit'},
                'wind': {'value': wind_value, 'units': 'miles/hour'},
                'temperature_feels_like':{'value': weather_info['currently']['apparentTemperature'], 'units': 'celsius'},
                                    # 'value': temperature_feels_like_value, 'units': 'fahrenheit'},
                'weather_condition': weather_info['currently']['icon']}
    return activity_weather


def get_weather_info_using_lat_lng_time(latitude, longitude, epoch_time, unit='si',include_block=['currently']):

    KEY = '52871e89c8acb84e7c8b8bc8ac5ba307'
    POSSIBLE_DATA_BLOCK = ['currently', 'minutely','hourly', 'daily', 'alerts','flags'] 
    UNITS = ['si', 'auto', 'ca', 'uk2', 'us']

    if include_block == []:
        include_block.append('currently')
    else:
        for item in include_block:
            if item not in POSSIBLE_DATA_BLOCK:
                raise ValueError ('Given {} is not present in include_block'.format(item))

    if unit == '':
        unit = 'si'
    elif unit not in UNITS:
        raise ValueError ('Given {} is not present in UNITS'.format(unit))
    
    EXCLUDE_KEYS = set(POSSIBLE_DATA_BLOCK)-set(include_block)
    URL = 'https://api.darksky.net/forecast/{}/{},{},{}?exclude={}&units={}'.format(
            KEY, latitude,longitude, epoch_time, ','.join(EXCLUDE_KEYS), unit)
    try:
        weather_report = requests.get(url=URL)
        return weather_report.json()
    except:
        return ()
