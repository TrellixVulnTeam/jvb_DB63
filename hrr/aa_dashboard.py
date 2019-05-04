

def aa_low_high_end_data(user,start_date):
	'''
		This function calculates the A/A third chart data
	''' 
	heart_rate_zone_low_end = ""
	heart_rate_zone_high_end = ""
	time_in_zone_for_last_7_days = ""
	prcnt_total_duration_in_zone = ""

	start_date_str = start_date.strftime('%Y-%m-%d')

	start_date_timestamp = start_date
	start_date_timestamp = start_date_timestamp.timetuple()
	start_date_timestamp = time.mktime(start_date_timestamp)
	end_date_timestamp = start_date_timestamp + 86400

	# activity_files_qs=UserGarminDataActivity.objects.filter(user= user,start_time_in_seconds__range=[start_date_timestamp,end_date_timestamp])
	# garmin_activity_keys = []
	# garmin_workout = []
	# if activity_files_qs:
	# 	activity_files = [pr.data for pr in activity_files_qs]
	# 	one_activity_file_dict =  ast.literal_eval(activity_files[0])
	# 	offset = one_activity_file_dict['startTimeOffsetInSeconds']
	# 	for i,single_activity in enumerate(activity_files):
	# 		one_activity_file =  ast.literal_eval(single_activity)
	# 		garmin_activity_keys.append(one_activity_file['summaryId'])
	# 		garmin_workout.append(one_activity_file)
	# else:
	# 	activity_files = ''
	# 	offset = 0
	# ui_data = _get_activities(user,start_date_str)
	# ui_data_keys = [ui_keys for ui_keys in ui_data.keys()]
	# ui_data_hrr = []
	# ui_data_keys_test = []

	# for ui_data_single in ui_data.values():
	# 	if ui_data_single.get(
	# 		'activityType') == 'HEART_RATE_RECOVERY':
	# 		summaryId = ui_data_single['summaryId']
	# 		ui_data_hrr.append(summaryId)
	# 	elif ui_data_single.get("duplicate") == False:
	# 			summaryId = ui_data_single['summaryId'] 
	# 			ui_data_keys_test.append(summaryId)
	garmin_list,garmin_dic = get_garmin_activities(
		user,start_date_timestamp,end_date_timestamp)
	manually_edited_dic,manually_edited_list = get_garmin_manully_activities(
		user,start_date_timestamp,end_date_timestamp)
	activities_dic = get_usernput_activities(
		user,start_date)

	user_age = user.profile.age()
	filtered_activities_files = get_filtered_activity_stats(activities_json=garmin_list,
													user_age=user_age,
													manually_updated_json=manually_edited_dic,
													userinput_activities=activities_dic,
													user=user,calendar_date=start_date)

	filtered_activities_only = get_filtered_activity_stats(activities_json=garmin_list,
													user_age=user_age,
													manually_updated_json=manually_edited_dic,
													user=user,calendar_date=start_date)
	activities = []
	hrr_summary_id = []
	workout_summary_id = []
	id_act = 0
	workout_data = []
	for i,k in enumerate(filtered_activities_files):
		if filtered_activities_files[i]['activityType'] == 'HEART_RATE_RECOVERY':
			id_act = int(filtered_activities_files[i]['summaryId'])
			activities.append(filtered_activities_files[i])
			hrr_summary_id.append(filtered_activities_files[i]['summaryId'])
		else:
			if filtered_activities_files[i]["duplicate"] == False:
				workout_data.append(filtered_activities_files[i])
				workout_summary_id.append(filtered_activities_files[i]['summaryId'])

	# user_created_activity = list(set(workout_summary_id)- set(garmin_activity_keys))
	garmin_workout_keys = set(garmin_activity_keys) - set(hrr_summary_id)
	# user_created_activity_list = []
	# if workout_data and user_created_activity:
	# 	for single_activity in workout_data:
	# 		for single_activity_key in user_created_activity:
	# 			if single_activity_key == single_activity['summaryId']:
	# 				user_created_activity_list.append(single_activity)

	# remove_in_workout = []
	# for i,single_actiivty in enumerate(filtered_activities_files):
	# 	if (single_actiivty.get("manual",0) == True 
	# 		and activities_dic
	# 		and activities_dic.get(single_actiivty["summaryId"])):

	# 		# user_created_activity_list.append(
	# 		# 	activities_dic.get(single_actiivty["summaryId"]))
	# 		for i,k in enumerate(filtered_activities_files):
	# 			garmin_id = single_actiivty.get("summaryId")
	# 			ui_id = filtered_activities_files[i].get('summaryId')
	# 			garmin_hr = single_actiivty.get("averageHeartRateInBeatsPerMinute",0)
	# 			ui_hr = filtered_activities_files[i].get("averageHeartRateInBeatsPerMinute",0)
	# 			garmin_duration = single_actiivty.get("durationInSeconds",0)
	# 			ui_duration = filtered_activities_files[i].get("durationInSeconds",0)
	# 			if ui_hr == None or ui_hr == '':
	# 				ui_hr = 0
	# 			if garmin_hr == None or garmin_hr == '':
	# 				garmin_hr = 0
	# 			if garmin_duration == None or garmin_duration == '':
	# 				garmin_duration = 0
	# 			if ui_duration == None or ui_duration == '':
	# 				ui_duration = 0
	# 			if (garmin_id == ui_id) and ((garmin_hr != ui_hr) or (garmin_duration != ui_duration)):
	# 				user_created_activity_list.append(k)
	# 				remove_in_workout.append(int(k["summaryId"]))

		# elif (single_actiivty.get("manual",0) != True 
		# 	and activities_dic
		# 	and activities_dic.get(single_actiivty["summaryId"])):
		# 	for i,k in enumerate(filtered_activities_files):
		# 		garmin_id = single_actiivty.get("summaryId")
		# 		ui_id = filtered_activities_files[i].get('summaryId')
		# 		garmin_hr = single_actiivty.get("averageHeartRateInBeatsPerMinute",0)
		# 		ui_hr = filtered_activities_files[i].get("averageHeartRateInBeatsPerMinute",0)
		# 		if ui_hr == None or ui_hr == '':
		# 			ui_hr = 0
		# 		if garmin_hr == None or garmin_hr == '':
		# 			garmin_hr = 0
		# 		if (garmin_id == ui_id) and ((not garmin_hr and ui_hr) or (garmin_hr != ui_hr)):
		# 			user_created_activity_list.append(k)
		# 			remove_in_workout.append(int(k["summaryId"]))

	# for i,single_activity in enumerate(filtered_activities_only):
	# 	avg_hr = single_activity.get('averageHeartRateInBeatsPerMinute',0)
	# 	summaryid = int(single_activity.get('summaryId',0))
	# 	if avg_hr == '' or avg_hr == 0 and summaryid not in remove_in_workout:
	# 		user_created_activity_list.append(single_activity)

	workout = []
	hrr = []
	start = start_date
	end = start_date + timedelta(days=3)
	fitfiles_obj = get_fitfiles(user,start_date,start,end,start_date_timestamp,end_date_timestamp)
	if activities_dic and fitfiles_obj:
		for tmp in fitfiles_obj:
			meta = tmp.meta_data_fitfile
			meta = ast.literal_eval(meta)
			data_id = meta['activityIds'][0]
			if str(data_id) in workout_summary_id and str(data_id) not in remove_in_workout:
				workout.append(tmp)
			elif str(data_id) in hrr_summary_id	:
				hrr.append(tmp)
	elif fitfiles_obj:
		for tmp in fitfiles_obj:
			meta = tmp.meta_data_fitfile
			meta = ast.literal_eval(meta)
			data_id = meta['activityIds'][0]
			if str(data_id) in workout_summary_id:
				workout.append(tmp)
			elif str(data_id) in hrr_summary_id:
				hrr.append(tmp)

	if workout:
		workout_data = fitfile_parse(workout,offset,start_date_str)
		workout_final_heartrate,workout_final_timestamp,workout_timestamp = workout_data
		for c,d in zip(workout_final_heartrate,workout_final_timestamp):
			