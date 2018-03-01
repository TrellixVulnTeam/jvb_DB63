from datetime import datetime, timedelta , date
import calendar
import ast
import time
import json
import xlsxwriter
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from xlsxwriter.workbook import Workbook
from user_input.models import DailyUserInputOptional ,\
                              DailyUserInputEncouraged,\
                              DailyUserInputStrong

from .serializers import UserQuickLookSerializer,\
						 GradesSerializer,\
						 StepsSerializer,\
						 SleepSerializer


from .models import UserQuickLook,\
					Grades,\
					Sleep,\
					Steps,\
					SwimStats,\
					BikeStats,\
					Food,\
					Alcohol,\
					ExerciseAndReporting

from progress_analyzer.models import OverallHealthGradeCumulative, \
                                     NonExerciseStepsCumulative,\
                                     SleepPerNightCumulative,\
                                     MovementConsistencyCumulative,\
                                     ExerciseConsistencyCumulative,\
                                     NutritionCumulative,\
                                     ExerciseStatsCumulative,\
                                     AlcoholCumulative,\
                                     OtherStatsCumulative





class UserQuickLookView(generics.ListCreateAPIView):
	'''
		- Create the quick look instance
		- List all the quick look instance
		- If query parameters "to" and "from" are provided
		  then filter the quick look data for provided date interval
		  and return the list
	'''
	permission_classes = (IsAuthenticated,)
	serializer_class = UserQuickLookSerializer

	def get_queryset(self):
		user = self.request.user

		end_dt = self.request.query_params.get('to',None)
		start_dt = self.request.query_params.get('from', None)

		if start_dt and end_dt:
			queryset = UserQuickLook.objects.filter(Q(created_at__gte=start_dt)&
							  Q(created_at__lte=end_dt),
							  user=user)
		else:
			queryset = UserQuickLook.objects.all()

		return queryset

class UserQuickLookItemView(generics.RetrieveUpdateDestroyAPIView):
	'''
		GET for getting particular model instance
		PUT for updating particular model instance
		DELETE for deleting particular model instance
		
		-displays only current user data not others (for now)
		-search item based on provided date
	'''
	permission_classes = (IsAuthenticated,)
	serializer_class = UserQuickLookSerializer

	def get_queryset(self):
		user = self.request.user
		qs = UserQuickLook.objects.filter(user=user)
		return qs

	def get_object(self):
		qs = self.get_queryset()
		d = int(self.kwargs.get('day'))
		m = int(self.kwargs.get('month'))
		y = int(self.kwargs.get('year'))
		dt = datetime.date(y,m,d)
		obj = get_object_or_404(qs,created_at=dt)
		return obj


class GradeItemView(generics.RetrieveUpdateDestroyAPIView):
	'''
		GET for getting particular model instance
		PUT for updating particular model instance
		DELETE for deleting particular model instance
		
		-displays only current user data not others (for now)
		-search item based on created date (for now)
	'''
	permission_classes = (IsAuthenticated,)
	serializer_class = GradesSerializer

	def get_queryset(self):
		user = self.request.user
		qs = Grades.objects.filter(user_ql__user=user)
		return qs

	def get_object(self):
		qs = self.get_queryset()
		d = int(self.kwargs.get('day'))
		m = int(self.kwargs.get('month'))
		y = int(self.kwargs.get('year'))
		dt = datetime.date(y,m,d)
		obj = get_object_or_404(qs,user_ql__created_at=dt)
		return obj

class GradeWeeklyListView(generics.ListAPIView):
	'''
		Return list of grades from last sunday to provided date
		Week start at Sunday and ends at Saturday
	'''
	permission_classes = (IsAuthenticated,)
	serializer_class = GradesSerializer

	def get_queryset(self):
		user = self.request.user
		d = int(self.kwargs.get('day'))
		m = int(self.kwargs.get('month'))
		y = int(self.kwargs.get('year'))
		current_dt = datetime.date(y,m,d)

		if not current_dt.weekday() == 6:
			week_start_dt = current_dt - datetime.timedelta(current_dt.weekday()+1)
		else:
			week_start_dt = current_dt
		
		qs = Grades.objects.filter(Q(user_ql__created_at__gte=week_start_dt)&
								   Q(user_ql__created_at__lte=current_dt),
								   user_ql__user=user,)
		return qs

class GradeListView(generics.ListCreateAPIView):
	permission_classes = (IsAuthenticated,)
	queryset = Grades.objects.all()
	serializer_class = GradesSerializer

class StepsItemView(generics.RetrieveUpdateDestroyAPIView):
	'''
		GET for getting particular model instance
		PUT for updating particular model instance
		DELETE for deleting particular model instance
		
		-displays only current user data not others (for now)
		-search item based on created date (for now)
	'''
	permission_classes = (IsAuthenticated,)
	serializer_class = StepsSerializer

	def get_queryset(self):
		user = self.request.user
		qs = Steps.objects.filter(user_ql__user=user)
		return qs

	def get_object(self):
		qs = self.get_queryset()
		d = int(self.kwargs.get('day'))
		m = int(self.kwargs.get('month'))
		y = int(self.kwargs.get('year'))
		dt = datetime.date(y,m,d)
		obj = get_object_or_404(qs,user_ql__created_at=dt)
		return obj

class StepListView(generics.ListCreateAPIView):
	permission_classes = (IsAuthenticated,)
	queryset = Steps.objects.all()
	serializer_class = StepsSerializer

class SleepItemView(generics.RetrieveUpdateDestroyAPIView):
	'''
		GET for getting particular model instance
		PUT for updating particular model instance
		DELETE for deleting particular model instance
		
		-displays only current user data not others (for now)
		-search item based on created date (for now)
	'''
	permission_classes = (IsAuthenticated,)
	serializer_class = SleepSerializer

	def get_queryset(self):
		user = self.request.user
		qs = Sleep.objects.filter(user_ql__user=user)
		return qs

	def get_object(self):
		qs = self.get_queryset()
		d = int(self.kwargs.get('day'))
		m = int(self.kwargs.get('month'))
		y = int(self.kwargs.get('year'))
		dt = datetime.date(y,m,d)
		obj = get_object_or_404(qs,user_ql__created_at=dt)
		return obj

class SleepListView(generics.ListCreateAPIView):
	permission_classes = (IsAuthenticated,)
	queryset = Sleep.objects.all()
	serializer_class = SleepSerializer

def export_users_xls(request):
	to_date1 = request.GET.get('to_date',None)
	from_date1 = request.GET.get('from_date', None)

	to_date = datetime.strptime(to_date1, "%m-%d-%Y").date()
	from_date = datetime.strptime(from_date1, "%m-%d-%Y").date()

	x= to_date.strftime('%m-%d-%y')
	# print(type(x))
	y= x.split("-")
	z = str(int(y[0]))+'-'+str(int(y[1]))+'-'+str(int(y[2]))

	# date_format_month = str(to_date.month)+'-'+str(to_date.day)+'-'+str(to_date.year)
	# print (date_format_month)

	filename = '{}_raw_data_{}_to_{}.xlsx'.format(request.user.username,
		from_date.strftime('%b_%d_%Y'),to_date.strftime('%b_%d_%Y'))
	response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
	response['Content-Disposition'] = "attachment; filename={}".format(filename) 
	book = Workbook(response,{'in_memory': True})
	sheet1 = book.add_worksheet('Grades')
	sheet2 = book.add_worksheet('Steps')
	sheet3 = book.add_worksheet('Sleep')
	sheet4 = book.add_worksheet('Food')
	sheet5 = book.add_worksheet('Alcohol')
	sheet6 = book.add_worksheet('Exercise Reporting')
	sheet7 = book.add_worksheet('Swim Stats')
	sheet8 = book.add_worksheet('Bike Stats')
	sheet9 = book.add_worksheet('All Stats')
	sheet1.set_column(1,1000,11)
	sheet2.set_column(1,1000,11)
	sheet3.set_column(1,1000,11)
	sheet4.set_column(1,1000,11)
	sheet5.set_column(1,1000,11)
	sheet6.set_column(1,1000,11)
	sheet7.set_column(1,1000,11)
	sheet8.set_column(1,1000,11)
	sheet9.set_column(1,1000,11)
	sheet1.freeze_panes(1, 1)
	sheet1.set_column('A:A',40)
	sheet2.freeze_panes(1, 1)
	sheet2.set_column('A:A',35)
	sheet3.freeze_panes(1, 1)
	sheet3.set_column('A:A',35)
	sheet4.freeze_panes(1, 1)
	sheet4.set_column('A:A',40)
	sheet5.freeze_panes(1, 1)
	sheet5.set_column('A:A',35)
	sheet6.freeze_panes(1, 1)
	sheet6.set_column('A:A',35)
	sheet7.freeze_panes(1, 1)
	sheet7.set_column('A:A',35)
	sheet8.freeze_panes(1, 1)
	sheet8.set_column('A:A',35)
	sheet9.freeze_panes(1, 1)
	sheet9.set_column('A:A',35)
	sheet9.repeat_rows(0)
	sheet9.repeat_columns(0)
	sheet9.set_row(33, 150)
	sheet9.set_landscape()
	sheet9.set_row(0,30)
	bold = book.add_format({'bold': True})
	date_format = book.add_format({'num_format': 'm-d-yy'})
	current_date = to_date
	format_week = book.add_format()
	format_week.set_align('top')
	format_week.set_text_wrap()
	format_week.set_shrink()
	r = 0
	if to_date and from_date :
		while (current_date >= from_date):
			r = r + 1
			weekday1 = calendar.day_name[current_date.weekday()]
			x= current_date.strftime('%m-%d-%y')
			current_date_split= x.split("-")
			current_date_string = str(int(current_date_split[0]))+'-'+str(int(current_date_split[1]))+'-'+str(current_date_split[2])
			current_date_string = str(current_date_string)
			result = [current_date_string]
			sheet9.write_rich_string(0,r,weekday1,'\n',current_date_string,format_week)
			# sheet9.write(0, r, current_date,date_format)
			current_date -= timedelta(days = 1)

	
	format_red = book.add_format({'align':'left', 'bg_color': 'red','num_format': '#,##0'})
	format_red_con = book.add_format({'align':'left', 'bg_color': 'red','num_format': '#,##0','font_color': 'white'})
	format_green = book.add_format({'align':'left', 'bg_color': 'green','num_format': '#,##0','font_color': 'white'})
	format_yellow = book.add_format({'align':'left', 'bg_color': 'yellow','num_format': '#,##0'})
	format_orange = book.add_format({'align':'left', 'bg_color': '#00B0EC','num_format': '#,##0'})
	format_purple = book.add_format({'align':'left', 'bg_color': 'pink','num_format': '#,##0','font_color': 'white'})
	format = book.add_format({'align':'left','num_format': '#,##0'})
	format1 = book.add_format({'align':'left','num_format': '0.00'})
	
	format_exe = book.add_format({'align':'left','num_format': '0.0'})
	format_red_a = book.add_format({'align':'left', 'bg_color': 'red','num_format': '0.0'})
	format_green_a = book.add_format({'align':'left', 'bg_color': 'green','num_format': '0.0','font_color': 'white'})
	format_yellow_a= book.add_format({'align':'left', 'bg_color': 'yellow','num_format': '0.0'})
	format_red_overall = book.add_format({'align':'left', 'bg_color': 'red','num_format': '0.00'})
	format_green_overall = book.add_format({'align':'left', 'bg_color': 'green','num_format': '0.00','font_color': 'white'})
	format_yellow_overall= book.add_format({'align':'left', 'bg_color': 'yellow','num_format': '0.00'})
	# Grades
	columns = ['overall_health_grade','overall_health_gpa','movement_non_exercise_steps_grade','non_exercise_steps',
			   'movement_consistency_grade','movement_consistency','avg_sleep_per_night_grade','sleep_per_wearable','exercise_consistency_grade',
			   'workout','exercise_consistency_score','prcnt_unprocessed_food_consumed_grade','prcnt_non_processed_food','alcoholic_drink_per_week_grade','alcohol_week',
			   'sleep_aid_penalty','ctrl_subs_penalty','smoke_penalty','overall_gpa_without_penalties']
	columnsw = ['Overall Health Grade','Overall Health Gpa','Non Exercise Steps Grade','Non Exercise Steps',
			   'Movement Consistency Grade','Movement Consistency Score','Avg Sleep Per Night Grade','Average Sleep Per Night',
			   'Exercise Consistency Grade',"Did you Workout Today",'Exercise Consistency Score','Percentage of Unprocessed Food Consumed Grade',
			   'Percentage of Unprocessed Food Consumed','Alcohol Drinks Consumed Per Last 7 Days Grade','Alcohol Drinks Consumed Per Last 7 Days'
			   ,'Sleep Aid Penalty','Controlled Substance Penalty','Smoking Penalty','Overall Health Grade Before Penalties','Did You Report Your Inputs Today?']

	colunn_work = ['workout']
	grades_qs = Grades.objects.filter(
		user_ql__created_at__range=(from_date, to_date),
		user_ql__user = request.user).order_by('-user_ql__created_at')
	grades_datewise = {q.user_ql.created_at.strftime("%Y-%m-%d"):q
		 for q in grades_qs}

	steps_qs = Steps.objects.filter(
		user_ql__created_at__range=(from_date, to_date),
		user_ql__user = request.user).order_by('-user_ql__created_at')

	steps_datewise = {q.user_ql.created_at.strftime("%Y-%m-%d"):q
		 for q in steps_qs }
	sleep_qs = Sleep.objects.filter(
		user_ql__created_at__range=(from_date, to_date),
		user_ql__user = request.user).order_by('-user_ql__created_at')

	sleep_datewise = {q.user_ql.created_at.strftime("%Y-%m-%d"):q
		 for q in sleep_qs }

	exercise_qs = ExerciseAndReporting.objects.filter(
		user_ql__created_at__range=(from_date, to_date),
		user_ql__user = request.user).order_by('-user_ql__created_at')

	exercise_datewise = {q.user_ql.created_at.strftime("%Y-%m-%d"):q
		 for q in exercise_qs }

	food_qs = Food.objects.filter(
		user_ql__created_at__range=(from_date, to_date),
		user_ql__user = request.user).order_by('-user_ql__created_at')

	food_datewise = {q.user_ql.created_at.strftime("%Y-%m-%d"):q
		 for q in food_qs }
	alcohol_qs = Alcohol.objects.filter(
		user_ql__created_at__range=(from_date, to_date),
		user_ql__user = request.user).order_by('-user_ql__created_at')

	options_user = DailyUserInputOptional.objects.filter(
		user_input__created_at__range=(from_date, to_date),
		user_input__user = request.user).order_by('-user_input__created_at')

	options_datewise = {q.user_input.created_at.strftime("%Y-%m-%d"):q
		 for q in options_user }

	alcohol_datewise = {q.user_ql.created_at.strftime("%Y-%m-%d"):q
		 for q in alcohol_qs}
	options_user_input = DailyUserInputEncouraged.objects.filter(
		user_input__created_at__range=(from_date, to_date),
		user_input__user = request.user).order_by('-user_input__created_at')
	options_user_input_datewise = {q.user_input.created_at.strftime("%Y-%m-%d"):q
		 for q in options_user_input }


	user_input_strong = DailyUserInputStrong.objects.filter(
		user_input__created_at__range=(from_date, to_date),
		user_input__user = request.user).order_by('-user_input__created_at')
	user_input_strong_datewise = {q.user_input.created_at.strftime("%Y-%m-%d"):q
		 for q in user_input_strong }

	health_grade_cum = OverallHealthGradeCumulative.objects.filter(
		user_cum__created_at__range=(from_date, to_date),
		user_cum__user = request.user).order_by('-user_cum__created_at')
	health_grade_cum_datewise = {q.user_cum.created_at.strftime("%Y-%m-%d"):q
		 for q in health_grade_cum }


	current_date = to_date
	r = 0
	if to_date and from_date:
		while (current_date >= from_date):
			r = r + 1
			# sheet2.write(0, r, current_date,date_format)
			current_date -= timedelta(days=1)
	sheet9.write(0, 0, "All Stats(month-day-year)",bold)
	sheet9.write(1, 0, "Grades",bold)
	sheet9.write(2, 0, "OVERALL HEALTH GRADES",bold)
	col_num1 = 2
	row_num = 0
	for col_num in range(len(columnsw)):
		col_num1 = col_num1 + 1
		sheet9.write(col_num1, row_num, columnsw[col_num])

	current_date = to_date
	i = 0
	while (current_date >= from_date):
		steps_data = steps_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		grades_data = grades_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		sleep_data = sleep_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		food_data = food_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		alcohol_data = alcohol_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		exercise_data = exercise_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		user_input_strong_data = user_input_strong_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		health_grade_cum = health_grade_cum_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		# print(health_grade_cum)
		if steps_data and grades_data and exercise_data and food_data and alcohol_data and sleep_data:
			if user_input_strong_data:
				user_input_strong_data = user_input_strong_data.__dict__
			steps_data = steps_data.__dict__
			grades_data = grades_data.__dict__
			sleep_data = sleep_data.__dict__
			exercise_data = exercise_data.__dict__
			alcohol_data = alcohol_data.__dict__
			food_data = food_data.__dict__
			# health_grade_cum = health_grade_cum.__dict__
			# logic
			# print(health_grade_cum)
			row_num += 1
			for i,key in enumerate(columns):
		
				if key != 'non_exercise_steps' and key != 'movement_consistency' and key != 'sleep_per_wearable' and key != 'prcnt_non_processed_food' and key != 'alcohol_week' and key != 'workout' and key != 'overall_gpa_without_penalties':
					if grades_data[key] == 'A':
						sheet9.write(i+3,row_num, grades_data[key],format_green)
					elif grades_data[key] == 'B':
						sheet9.write(i+3,row_num, grades_data[key],format_green)
					elif grades_data[key] == 'C':
						sheet9.write(i+3,row_num, grades_data[key],format_yellow)
					elif grades_data[key] == 'D':
						sheet9.write(i+3,row_num, grades_data[key],format_yellow)
					elif grades_data[key] == 'F':
						sheet9.write(i+3,row_num, grades_data[key],format_red)
					elif grades_data[key] == 'N/A':
						sheet9.write(i+3,row_num, grades_data[key],format1)
					elif i == 10:
						sheet9.write(i+3,row_num, grades_data[key],format_exe)
					elif key == 'sleep_aid_penalty' or key == 'ctrl_subs_penalty' or key == 'smoke_penalty':
						if grades_data[key] == 0:
							sheet9.write(i+3,row_num, 'NO',format1)
						else:	
							sheet9.write(i+3,row_num, 'YES',format_red)
					elif i == 1:
						sheet9.write(i+3,row_num, grades_data[key],format1)
					elif grades_data[key] == '':
						sheet9.write(i+3,row_num,"Not Reported")

				elif key == '':
					sheet9.write(i+3,row_num, 'Not Reported',format1)
				elif i == 3:
					sheet9.write(i+3,row_num, steps_data[key],format)
				elif i == 5 and key == 'movement_consistency' and steps_data[key]:
					sheet9.write(i+3,row_num, ast.literal_eval(steps_data[key])['inactive_hours'],format)
				elif i == 7:
					if user_input_strong_data:
						avg_sleep = user_input_strong_data['sleep_time_excluding_awake_time']
						if avg_sleep and avg_sleep != ":":
							sheet9.write(i+3,row_num, user_input_strong_data['sleep_time_excluding_awake_time'],format1)
						else:
							sheet9.write(i+3,row_num, sleep_data[key],format1)
					else:
						sheet9.write(i+3,row_num, sleep_data[key],format1)
					# if user_input_strong_data:
					# 	print("exists")
					# else:
					# 	print("Does not exits")
				elif key == 'workout' and i == 9:
					if user_input_strong_data:
						sheet9.write(i+3, row_num, user_input_strong_data[key],format)
						# if key == 19:
						# 	sheet9.write(i+3,row_num,"Yes")
						# else:
						# 	sheet9.write(i+3,row_num,"No",format_red)
					else:
						sheet9.write(i+3, row_num," ",format)
				elif i == 12:
					if food_data[key] == '':
						
						sheet9.write(i+3,row_num, '')
					else:
						sheet9.write(i+3,row_num, str(int(food_data[key])) + '%')
				elif i == 14:
					sheet9.write(i+3,row_num, alcohol_data[key],format_exe)
				elif i == 18:
					grade_point = {"A":4,"B":3,"C":2,"D":1,"F":0,"":0}
					# overall_workout_gpa_cal = grades_data['overall_health_gpa']
					# sleep_aid_penalty_cal = grades_data['sleep_aid_penalty']
					# ctrl_subs_penalty_cal = grades_data['ctrl_subs_penalty']
					# smoke_penalty_cal = grades_data['smoke_penalty']
					grades_steps = grades_data['movement_non_exercise_steps_grade']
					grades_consistency = grades_data['movement_consistency_grade']
					grades_sleep = grades_data['avg_sleep_per_night_grade']
					grades_consistency_exe = grades_data['exercise_consistency_grade']
					grades_food = grades_data['prcnt_unprocessed_food_consumed_grade']
					grades_alcohol = grades_data['alcoholic_drink_per_week_grade']
					overall_workout_gpa_without_penalty = (grade_point[grades_steps]+grade_point[grades_consistency]+
					grade_point[grades_sleep]+grade_point[grades_consistency_exe]+grade_point[grades_food]+grade_point[grades_alcohol])/6
					if overall_workout_gpa_without_penalty >= 3:
						sheet9.write(i+3,row_num,overall_workout_gpa_without_penalty,format_green_overall)
					elif overall_workout_gpa_without_penalty >= 1 and overall_workout_gpa_without_penalty < 3:
						sheet9.write(i+3,row_num,overall_workout_gpa_without_penalty,format_yellow_overall)
					elif overall_workout_gpa_without_penalty < 1:
						sheet9.write(i+3,row_num,overall_workout_gpa_without_penalty,format_red_overall)


					# overall_workout_gpa_without_penalty = overall_workout_gpa_cal+sleep_aid_penalty_cal+ctrl_subs_penalty_cal+smoke_penalty_cal
					# sheet9.write(i+3,row_num,overall_workout_gpa_without_penalty,format1)

				else:
					sheet9.write(i+3,row_num, 'Not Reported')
				# if key == 19:
				# 	sheet9.write(i+3,row_num,"Yes")
				# else:
				# 	sheet9.write(i+3,row_num,"No",format_red)
			for i,key in enumerate(colunn_work):
				if user_input_strong_data:
					sheet9.write(22,row_num,"Yes")
				else:
					sheet9.write(22,row_num,"No",format_red)
		else:
			row_num += 1
			sheet9.write(i+3,row_num, '')
		current_date -= timedelta(days=1)

	# columnsg2 = ['Resting Heart Rate','Stress Level','Did you Stand for 3 hours or more above and beyond your exercise yesterday?']
	# col = ['sleep_resting_hr_last_night','stress_level','stand_for_three_hours']
	# sheet1.write(21, 0, "NOT GRADED CATEGORIES",bold)
	# col_num2 = 21
	# num_10 = row_num
	# len_gra = len(rows_of_grades)
	# for col_num in range(len(columnsg2)):
	# 	 col_num2 = col_num2 + 1
	# 	 sheet1.write(col_num2,row_num - num_10, columnsg2[col_num])


	# current_date = to_date
	# while (current_date >= from_date):
	# 	options_data = options_datewise.get(current_date.strftime("%Y-%m-%d"),None)
	# 	exercise_data = exercise_datewise.get(current_date.strftime("%Y-%m-%d"),None)
	# 	if options_data and exercise_data:
	# 		options_data = options_data.__dict__
	# 		exercise_data = exercise_data.__dict__
	# 		# logic
	# 		row_num += 1
	# 		for i, key in enumerate(col):
	# 			if key == 'stand_for_three_hours':
	# 				sheet1.write(col_num2+i-2, row_num - num_10, options_data[key],format)
	# 			else:
	# 				sheet1.write(col_num2+i-2, row_num - num_10, exercise_data[key],format)
	# 	else:
	# 		# print("no data")
	# 		row_num += 1
	# 		sheet1.write(col_num2+i-2, row_num - num_10, '')
	# 	current_date -= timedelta(days=1)
	
	# sheet1.write(26, 0, "PERFORMANCE ASSESSMENT",bold)
	# columnsg3 = ['Overall Workout Grade ','Overall Workout Score (points)','Workout Duration Grade','Workout Duration'
	# ,'Workout Effort Level Grade','Workout Effort Level','Average Exercise Heart Rate Grade ','Average Exercise Heart Rate'
	# ,'Heart Rate Recovery (HRR) - time to 99','Heart Rate Recovery (HRR) - heart beats lowered in the first minute '
	# ,'VO2 Max','Floors Climbed ']
	# columnsg4 = ['overall_workout_grade','overall_workout_gpa','workout_duration_grade','workout_duration',
	# 'workout_effortlvl_grade','workout_effortlvl_gpa','avg_exercise_hr_grade','avg_exercise_hr_gpa','time_to_99',
	# 'lowest_hr_first_minute','vo2_max','floor_climed']
	# col_num2 = 26
	# len_gra1 = len(rows_of_grades) + len(exec1) 
	# num_1 = row_num
	# for col_num in range(len(columnsg3)):
	# 	 col_num2 = col_num2 + 1
	# 	 sheet1.write(col_num2,row_num - num_1, columnsg3[col_num])
	# l2 = 26
	# num_2 = row_num


	# current_date = to_date
	# while (current_date >= from_date):
	# 	options_user_data = options_user_input_datewise.get(current_date.strftime("%Y-%m-%d"),None)
	# 	exercise_data = exercise_datewise.get(current_date.strftime("%Y-%m-%d"),None)
	# 	grades_data = grades_datewise.get(current_date.strftime("%Y-%m-%d"),None)
	# 	steps_data = steps_datewise.get(current_date.strftime("%Y-%m-%d"),None)
	# 	if exercise_data and grades_data and steps_data:
	# 		if options_user_data:
	# 			options_user_data = options_user_data.__dict__
	# 		exercise_data = exercise_data.__dict__
	# 		grades_data = grades_data.__dict__
	# 		steps_data = steps_data.__dict__
	# 		# logic
	# 		row_num += 1
	# 		for i, key in enumerate(columnsg4):
	# 			if key != 'workout_duration' and key != 'floor_climed' and key != 'vo2_max' and key != 'lowest_hr_first_minute' and key != 'time_to_99':
	# 				if grades_data[key] == 'A':
	# 					sheet1.write(l2+i+1,row_num-num_2, grades_data[key],format_green)
	# 				elif grades_data[key] == 'B':
	# 					sheet1.write(l2+i+1,row_num-num_2, grades_data[key],format_green)
	# 				elif grades_data[key] == 'C':
	# 					sheet1.write(l2+i+1,row_num-num_2, grades_data[key],format_yellow)
	# 				elif grades_data[key] == 'D':
	# 					sheet1.write(l2+i+1,row_num-num_2, grades_data[key],format_yellow)
	# 				elif grades_data[key] == 'F':
	# 					sheet1.write(l2+i+1,row_num-num_2, grades_data[key],format_red)
	# 				elif grades_data[key] == 'N/A':
	# 					sheet1.write(l2+i+1,row_num-num_2, grades_data[key],format1)
	# 				elif grades_data[key] == '':
	# 					sheet1.write(l2+i+1,row_num-num_2, grades_data[key],format1)
	# 				else:
	# 					sheet1.write(l2+i+1,row_num-num_2, grades_data[key],format1)
	# 			elif key == 'workout_duration':
	# 				sheet1.write(l2+i+1, row_num-num_2, exercise_data[key],format)
	# 			elif key == 'floor_climed':
	# 				sheet1.write(l2+i+1, row_num-num_2, steps_data[key],format)
	# 			elif key == 'vo2_max':
	# 				sheet1.write(l2+i+1, row_num-num_2, exercise_data[key],format)
	# 			elif key == 'lowest_hr_first_minute':
	# 				if options_user_data:
	# 					sheet1.write(l2+i+1, row_num-num_2, options_user_data[key],format)
	# 				else:
	# 					sheet1.write(l2+i+1, row_num-num_2," ",format)
	# 			elif key == 'time_to_99':
	# 				if options_user_data:
	# 					sheet1.write(l2+i+1, row_num-num_2, options_user_data[key],format)
	# 				else:
	# 					sheet1.write(l2+i+1, row_num-num_2," ",format)
	# 			else:
	# 				sheet1.write(l2+i+1,row_num-num_2, 'YES',format_red)
	# 	else:
	# 		row_num += 1
	# 		sheet1.write(col_num2+i-2, row_num - num_2, '')
	# 	current_date -= timedelta(days=1)

	
	
	# Steps
	num_3 = row_num
	columns4 = ['movement_consistency','non_exercise_steps', 'exercise_steps', 'total_steps', 'floor_climed']
	columns4W = ['Movement Consistency','Non Exercise Steps', 'Exercise Steps', 'Total Steps', 'Floors Climed']
	sheet9.write(24, 0, "Steps",bold)
	col_num2 = 24
	# a = len(rows_of_grades)
	for col_num in range(len(columns4W)):
		 col_num2 = col_num2 + 1
		 sheet9.write(col_num2,row_num - num_3, columns4W[col_num])
	# i1 = 40
	# a = len(rows_of_grades)
	num_3 = row_num

	steps_qs = Steps.objects.filter(
		user_ql__created_at__range=(from_date, to_date),
		user_ql__user = request.user).order_by('-user_ql__created_at')

	steps_datewise = {q.user_ql.created_at.strftime("%Y-%m-%d"):q
		 for q in steps_qs }


	current_date = to_date
	i1 = 24
	while (current_date >= from_date):
		steps_data = steps_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		grades_data = grades_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		if steps_data and grades_data:
			steps_data = steps_data.__dict__
			grades_data = grades_data.__dict__
			# logic
			i1 = 24
			row_num += 1
			for i,key in enumerate(columns4):
				if i == 1 and grades_data['movement_non_exercise_steps_grade'] == 'A':
					sheet9.write(i1+i+1,row_num - num_3, steps_data[key], format_green)
				elif i == 1 and grades_data['movement_non_exercise_steps_grade'] == 'B':
					sheet9.write(i1+i+1,row_num - num_3, steps_data[key], format_green)
				elif i == 1 and grades_data['movement_non_exercise_steps_grade'] == 'C':
					sheet9.write(i1+i+1,row_num - num_3, steps_data[key], format_yellow)
				elif i == 1 and grades_data['movement_non_exercise_steps_grade'] == 'D':
					sheet9.write(i1+i+1,row_num - num_3, steps_data[key], format_yellow)
				elif i == 1 and grades_data['movement_non_exercise_steps_grade'] == 'F':
					sheet9.write(i1+i+1,row_num - num_3, steps_data[key], format_red)
				elif i == 0 and grades_data['movement_consistency_grade'] == 'A' and key == 'movement_consistency' and steps_data[key]:
					sheet9.write(i1+i+1,row_num - num_3, ast.literal_eval(steps_data[key])['inactive_hours'], format_green)
				elif i == 0 and grades_data['movement_consistency_grade'] == 'B' and key == 'movement_consistency' and steps_data[key]:
					sheet9.write(i1+i+1,row_num - num_3, ast.literal_eval(steps_data[key])['inactive_hours'], format_green)
				elif i == 0 and grades_data['movement_consistency_grade'] == 'C' and key == 'movement_consistency' and steps_data[key]:
					sheet9.write(i1+i+1,row_num - num_3, ast.literal_eval(steps_data[key])['inactive_hours'], format_yellow)
				elif i == 0 and grades_data['movement_consistency_grade'] == 'D' and key == 'movement_consistency' and steps_data[key]:
					sheet9.write(i1+i+1,row_num - num_3, ast.literal_eval(steps_data[key])['inactive_hours'], format_yellow)
				elif i == 0 and grades_data['movement_consistency_grade'] == 'F' and key == 'movement_consistency' and steps_data[key]:
					sheet9.write(i1+i+1,row_num - num_3,ast.literal_eval(steps_data[key])['inactive_hours'], format_red)
				else:
					sheet9.write(i1+i+1,row_num - num_3, steps_data[key], format)
		else:
			row_num += 1
			sheet9.write(i1+i+1,row_num - num_3, '')
		current_date -= timedelta(days=1)



	#Sleep

	columns5 = ['sleep_per_wearable','sleep_comments',  'sleep_aid','resting_hr_last_night','sleep_per_wearable', 'sleep_bed_time', 
	'sleep_awake_time','deep_sleep','light_sleep','awake_time']
	columns5W = ['Sleep Per User Input (excluding awake time)','Sleep Comments', 'Sleep Aid taken?', 
	'Resting Heart Rate (RHR)','Sleep per Wearable (excluding awake time)',
	'Sleep Bed Time', 'Sleep Awake Time','Deep Sleep','Light Sleep','Awake Time']
	sheet9.write(31, 0, "Sleep",bold)
	col_num2 = 31
	num_4 = row_num
	# a = len(rows_of_grades) + len(rows3)
	for col_num in range(len(columns5W)):
		col_num2 = col_num2 + 1
		sheet9.write(col_num2, row_num - num_4 , columns5W[col_num])
	
	# rows4hr = ExerciseAndReporting.objects.filter(
	# 	user_ql__created_at__range=(from_date, to_date),
	# 	user_ql__user = request.user).order_by('-user_ql__created_at').values()
	# i1 = 47
	format2 = book.add_format()
	format2.set_align('top')
	format2.set_text_wrap()
	format2.set_shrink()
	# sleep_qs = Sleep.objects.filter(
	# 	user_ql__created_at__range=(from_date, to_date),
	# 	user_ql__user = request.user).order_by('-user_ql__created_at')

	# sleep_datewise = {q.user_ql.created_at.strftime("%Y-%m-%d"):q
	# 	 for q in sleep_qs }

	# exercise_qs = ExerciseAndReporting.objects.filter(
	# 	user_ql__created_at__range=(from_date, to_date),
	# 	user_ql__user = request.user).order_by('-user_ql__created_at')

	# exercise_datewise = {q.user_ql.created_at.strftime("%Y-%m-%d"):q
	# 	 for q in exercise_qs }


	current_date = to_date
		
	while (current_date >= from_date):
		sleep_data = sleep_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		exercise_data = exercise_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		grades_data = grades_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		user_input_strong_data = user_input_strong_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		if sleep_data and exercise_data and grades_data:
			if user_input_strong_data:
				user_input_strong_data = user_input_strong_data.__dict__
			sleep_data = sleep_data.__dict__
			grades_data = grades_data.__dict__
			exercise_data = exercise_data.__dict__
			# logic
			i1 = 31
			row_num += 1
			for i, key in enumerate(columns5):
				if user_input_strong_data:
					if i == 0 and grades_data['avg_sleep_per_night_grade'] == 'A':
						sheet9.write(i1 + i + 1, row_num - num_4, user_input_strong_data['sleep_time_excluding_awake_time'], format_green)
					elif i == 0 and grades_data['avg_sleep_per_night_grade'] == 'B':
						sheet9.write(i1 + i + 1, row_num - num_4, user_input_strong_data['sleep_time_excluding_awake_time'], format_green)
					elif i == 0 and grades_data['avg_sleep_per_night_grade'] == 'C':
						sheet9.write(i1 + i + 1, row_num - num_4, user_input_strong_data['sleep_time_excluding_awake_time'], format_yellow)
					elif i == 0 and grades_data['avg_sleep_per_night_grade'] == 'D':
						sheet9.write(i1 + i + 1, row_num - num_4, user_input_strong_data['sleep_time_excluding_awake_time'], format_yellow)
					elif i == 0 and grades_data['avg_sleep_per_night_grade'] == 'F':
						sheet9.write(i1 + i + 1, row_num - num_4, user_input_strong_data['sleep_time_excluding_awake_time'], format_red)
				elif i == 1:
					sheet9.write(i1 + i + 1, row_num - num_4, sleep_data[key], format2)
				elif i == 3:
					if exercise_data[key] >= 76:
						sheet9.write(i1 + i + 1, row_num - num_4, exercise_data[key], format_red)
					if exercise_data[key] >= 63 and exercise_data[key] <= 75:
						sheet9.write(i1 + i + 1, row_num - num_4, exercise_data[key], format_yellow)
					if exercise_data[key] > 30 and exercise_data[key] <= 62:
						sheet9.write(i1 + i + 1, row_num - num_4, exercise_data[key], format_green)
					if exercise_data[key] <= 30:
						sheet9.write(i1 + i + 1, row_num - num_4, exercise_data[key], format_red)
				elif i != 0:
					sheet9.write(i1 + i + 1, row_num - num_4, sleep_data[key], format)
		else:
			row_num += 1
			sheet9.write(i1+i+1,row_num - num_4, '')
		current_date -= timedelta(days=1)
	#Food
	num_5 = row_num
	columns6 = ['prcnt_non_processed_food','processed_food','non_processed_food', 'diet_type']
	columns6W = ['% of Unprocessed Food','Processed Food Consumed', 'Non Processed Food', 'Diet Type']
	sheet9.write(43, 0, "Food",bold)
	col_num2 = 43
	# a = len(rows_of_grades) + len(rows3) + len(rows4)
	for col_num in range(len(columns6W)):
		col_num2 = col_num2 + 1
		sheet9.write(col_num2, row_num - num_5, columns6W[col_num])

	# food_qs = Food.objects.filter(
	# 	user_ql__created_at__range=(from_date, to_date),
	# 	user_ql__user = request.user).order_by('-user_ql__created_at')

	# food_datewise = {q.user_ql.created_at.strftime("%Y-%m-%d"):q
	# 	 for q in food_qs }


	current_date = to_date
	while (current_date >= from_date):
		food_data = food_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		grades_data = grades_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		if food_data and grades_data:
			food_data = food_data.__dict__
			grades_data = grades_data.__dict__
			# logic
			i1 = 43
			row_num += 1
			for i, key in enumerate(columns6):
				if grades_data['prcnt_unprocessed_food_consumed_grade'] == 'A' and i == 0:
					sheet9.write(i1 + i + 1, row_num - num_5,str(int(food_data[key])) + '%' ,format_green)
				elif grades_data['prcnt_unprocessed_food_consumed_grade'] == 'B' and i == 0:
					sheet9.write(i1 + i + 1, row_num - num_5, str(int(food_data[key])) + '%' ,format_green)
				elif grades_data['prcnt_unprocessed_food_consumed_grade'] == 'C' and i == 0:
					sheet9.write(i1 + i + 1, row_num - num_5,str(int(food_data[key])) + '%' ,format_yellow)
				elif grades_data['prcnt_unprocessed_food_consumed_grade'] == 'D' and i == 0:
					sheet9.write(i1 + i + 1, row_num - num_5, str(int(food_data[key])) + '%' ,format_yellow)
				elif grades_data['prcnt_unprocessed_food_consumed_grade'] == 'F' and i == 0:
					sheet9.write(i1 + i + 1, row_num - num_5,str(int(food_data[key])) + '%' ,format_red)
				elif grades_data['prcnt_unprocessed_food_consumed_grade'] == '':
					sheet9.write(i1 + i + 1, row_num - num_5,'',)
				else:
					sheet9.write(i1 + i + 1, row_num - num_5, food_data[key], format)
		else:
	
			row_num += 1
			sheet9.write(i1+i+1,row_num - num_5, '')
		current_date -= timedelta(days=1)


	#Alcohol
	num_6 = row_num
	columns7 = ['alcohol_day', 'alcohol_week']
	columns7W = ['# of Alcohol Drinks Consumed Yesterday', '# of Alcohol Drinks Consumed over last  7 Days']
	sheet9.write(49, 0, "Alcohol",bold)
	col_num2 = 49
	# a = len(rows_of_grades) + len(rows3) + len(rows4) + len(rows5)
	for col_num in range(len(columns7W)):
		   col_num2 = col_num2 + 1
		   sheet9.write(col_num2, row_num - num_6, columns7W[col_num])

	# alcohol_qs = Alcohol.objects.filter(
	# 	user_ql__created_at__range=(from_date, to_date),
	# 	user_ql__user = request.user).order_by('-user_ql__created_at')

	# grades_qs = Grades.objects.filter(
	# 	user_ql__created_at__range=(from_date, to_date),
	# 	user_ql__user = request.user).order_by('-user_ql__created_at')

	alcohol_datewise = {q.user_ql.created_at.strftime("%Y-%m-%d"):q
		 for q in alcohol_qs}	
	grades_datewise = {q.user_ql.created_at.strftime("%Y-%m-%d"):q
		 for q in grades_qs}	

	current_date = to_date
	while (current_date >= from_date):
		alcohol_data = alcohol_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		grades_data = grades_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		if alcohol_data and grades_data:
			alcohol_data = alcohol_data.__dict__
			grades_data = grades_data.__dict__
			# logic
			i1 = 49
			row_num += 1
			for i, key in enumerate(columns7):
				if i == 1 and grades_data['alcoholic_drink_per_week_grade'] == 'A':
					sheet9.write(i1 + i + 1, row_num - num_6, alcohol_data[key], format_green)
				elif i == 1 and grades_data['alcoholic_drink_per_week_grade'] == 'B':
					sheet9.write(i1 + i + 1, row_num - num_6, alcohol_data[key], format_green)
				elif i == 1 and grades_data['alcoholic_drink_per_week_grade'] == 'C':
					sheet9.write(i1 + i + 1, row_num - num_6, alcohol_data[key], format_yellow)
				elif i == 1 and grades_data['alcoholic_drink_per_week_grade'] == 'D':
					sheet9.write(i1 + i + 1, row_num - num_6, alcohol_data[key], format_yellow)
				elif i == 1 and grades_data['alcoholic_drink_per_week_grade'] == 'F':
					sheet9.write(i1 + i + 1, row_num - num_6, alcohol_data[key], format_red)
				else:
					sheet9.write(i1 + i + 1, row_num - num_6, alcohol_data[key],format)
		else:
			
			row_num += 1
			sheet9.write(i1+i+1,row_num - num_6, '')
		current_date -= timedelta(days=1)

	# Exercise Reporting

	columns_of_exercise = ["workout_easy_hard","workout_type","workout_time", "workout_location","workout_duration","maximum_elevation_workout","minutes_walked_before_workout",
	"distance_run","distance_bike","distance_swim","distance_other","pace","avg_heartrate","avg_heartrate","avg_heartrate",
	"elevation_gain","elevation_loss","effort_level","dew_point","temperature","humidity",
	"temperature_feels_like","wind","hrr_time_to_99","hrr_starting_point","hrr_beats_lowered_first_minute","resting_hr_last_night","vo2_max","running_cadence",
	"nose_breath_prcnt_workout","water_consumed_workout","chia_seeds_consumed_workout","fast_before_workout","pain","pain_area","stress_level","sick","drug_consumed",
	"drug","medication","smoke_substance","exercise_fifteen_more","workout_elapsed_time","timewatch_paused_workout","exercise_consistency",
	"heartrate_variability_stress","fitness_age","workout_comment"]
	columns8w = ['Workout Easy Hard','Workout Type', 'Workout Time','Workout Location','Workout Duration (hh:mm:ss)','Maximum Elevation Workout','Minutes Walked Before Workout','Distance (In Miles) - Run', 
	'Distance (in Miles) - Bike', 'Distance (in yards) - Swim', 'Distance (in Miles) - Other','Pace (minutes:seconds) (Running)','Average Heartrate RUNNING','Average Heartrate ELLIPTICAL','Average Heartrate OTHER','Elevation Gain(feet)','Elevation Loss(feet)', 
	'Effort Level','Dew Point (in °F)','Temperature (in °F)','Humidity (in %)',  'Temperature Feels Like (in °F)', 'Wind (in miles per hour)','HRR - Time to 99 (mm:ss)','HRR Start Point',  'HRR Beats Lowered','Sleep Resting Hr Last Night',
	'Vo2 Max','Running Cadence','Percent Breath through Nose During Workout','Water Consumed during Workout','Chia Seeds consumed during Workout','Fast Before Workout', 'Pain','Pain Area','Stress Level','Sick ', 'Drug Consumed',
	'Drug','Medication','Smoke Substance', 'Exercise Fifteen More','Workout Elapsed Time','TimeWatch Paused Workout','Exercise Consistency','Heart Rate Variability Stress (Garmin)','Fitness Age','Workout Comment']
	
	current_date = to_date
	r = 0
	if to_date and from_date:
		while (current_date >= from_date):
			r = r + 1
			# sheet9.write(0, r, current_date,date_format)
			current_date -= timedelta(days=1)
	num_11 = row_num
	sheet9.write(53, 0, "Exercise Reporting",bold)
	col_num1 = 53
	for col_num in range(len(columns8w)):
		col_num1 = col_num1 + 1
		sheet9.write(col_num1, row_num-num_11, columns8w[col_num])
	i1 = 53
	current_date = to_date
	while (current_date >= from_date):
		# logic
		data = exercise_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		if data:
			data = data.__dict__
			row_num += 1
			# for i,key in enumerate(columns_of_exercise):
			# 	if data[key] == None:
			# 		sheet9.write(i1+i+1,row_num - num_11,'Not Reported',format)
			# 	else:
			# 		sheet9.write(i1+i+1,row_num - num_11, data[key],format)
			for i,key in enumerate(columns_of_exercise):
				avg_heart_rate_string = data['avg_heartrate']
				json2_data = json.loads(avg_heart_rate_string)
				
				if i == 12:
					if 'RUNNING' in json2_data:
					 	sheet9.write(i1+i+1,row_num - num_11,json2_data['RUNNING'],format)
					else:
					 	sheet9.write(i1+i+1,row_num - num_11,"",format)
				elif i == 13:
					if 'ELLIPTICAL' in json2_data:
					 	sheet9.write(i1+i+1,row_num - num_11,json2_data['ELLIPTICAL'],format)
					else:
					 	sheet9.write(i1+i+1,row_num - num_11,"",format)
				elif i == 14:
					if 'OTHER' in json2_data:
					 	sheet9.write(i1+i+1,row_num - num_11,json2_data['OTHER'],format)
				elif data[key] == None:
					sheet9.write(i1+i+1,row_num - num_11,'Not Reported')
				elif key != 'avg_heartrate':
					sheet9.write(i1+i+1,row_num - num_11,data[key],format)
		else:
			row_num += 1
			sheet9.write(i1+i+1,row_num - num_11, '')
		current_date -= timedelta(days=1)


	# Swim status
	num_7 = row_num
	columns1 = ['pace_per_100_yard','total_strokes']
	columns1W = ['Pace Per 100 Yard','Total Strokes']
	sheet9.write(103, 0, "Swim Stats",bold)
	col_num2 = 103
	# a = len(rows_of_grades) + len(rows3) + len(rows4) + len(rows5) + len(rows6)
	for col_num1 in range(len(columns1W)):
			col_num2 = col_num2 + 1
			sheet9.write(col_num2 , row_num - num_7  , columns1W[col_num1],format)
	swim_qs = SwimStats.objects.filter(
		user_ql__created_at__range=(from_date, to_date),
		user_ql__user = request.user).order_by('-user_ql__created_at')

	swim_datewise = {q.user_ql.created_at.strftime("%Y-%m-%d"):q
		 for q in swim_qs }

	current_date = to_date
	for row in swim_qs.values():
		
		while (current_date >= from_date):
			data = swim_datewise.get(current_date.strftime("%Y-%m-%d"),None)
			if data:
				# logic
				i1 = 103
				row_num += 1
				for i,key in enumerate(columns1):
					sheet9.write(i1+i+1,row_num - num_7, row[key],format)
			else:
				row_num += 1
				sheet9.write(i1+i+1,row_num - num_7, '')
			current_date -= timedelta(days=1)

	# Bike
	num_8 = row_num
	columns3 = ['avg_speed', 'avg_power','avg_speed_per_mile','avg_cadence']
	columns3W = ['Avg Speed (MPH) Bike', 'Avg Power Bike','Avg_Speed Per Mile','Avg Cadence Bike']
	sheet9.write(107, 0, "Bike Stats",bold)
	col_num2 = 107
	# a = len(rows_of_grades) + len(rows3) + len(rows4) + len(rows5) + len(rows6) + len(rows1)
	for col_num in range(len(columns3W)):
		col_num2 = col_num2 + 1
		sheet9.write(col_num2, row_num - num_8, columns3W[col_num],format)

	bike_qs = BikeStats.objects.filter(
		user_ql__created_at__range=(from_date, to_date),
		user_ql__user = request.user).order_by('-user_ql__created_at')

	bike_datewise = {q.user_ql.created_at.strftime("%Y-%m-%d"):q
		 for q in bike_qs }

		
	current_date = to_date
	for row in bike_qs.values():

		while (current_date >= from_date):
			# logic
			data = bike_datewise.get(current_date.strftime("%Y-%m-%d"),None)
			if data:
				i1 = 107
			# for row in bike_qs.values():
				row_num += 1
				for i,key in enumerate(columns3):
					sheet9.write(i1+i+1,row_num - num_8, row[key],format)
			else:
				row_num += 1
				sheet9.write(i1+i+1,row_num - num_8, '')
			current_date -= timedelta(days=1)

	#Grades sheet
	sheet1.repeat_rows(0)
	sheet1.repeat_columns(0)
	sheet1.set_landscape()
	format2 = book.add_format()
	format2.set_align('top')
	format2.set_text_wrap()
	format2.set_shrink()
	sheet1.set_row(0, 30)
	# columns = ['overall_health_grade','overall_health_gpa','movement_non_exercise_steps_grade','non_exercise_steps',
	# 		   'movement_consistency_grade','movement_consistency','avg_sleep_per_night_grade','sleep_per_wearable','exercise_consistency_grade',
	# 		   'workout','exercise_consistency_score','prcnt_unprocessed_food_consumed_grade','prcnt_non_processed_food','alcoholic_drink_per_week_grade','alcohol_week',
	# 		   'sleep_aid_penalty','ctrl_subs_penalty','smoke_penalty']
	# columnsw = ['Overall Health Grade','Overall Health Gpa','Non Exercise Steps Grade','Non Exercise Steps',
	# 		   'Movement Consistency Grade','Movement Consistency Score','Avg Sleep Per Night Grade','Average Sleep Per Night',
	# 		   'Exercise Consistency Grade','Did you Workout Today','Exercise Consistency Score','Percentage of Unprocessed Food Consumed Grade',
	# 		   'Percentage of Unprocessed Food Consumed','Alcohol Drinks Consumed Per Last 7 Days Grade','Alcohol Drinks Consumed Per Last 7 Days'
	# 		   ,'Sleep Aid Penalty','Controlled Substance Penalty','Smoking Penalty']

	current_date = to_date
	r = 0
	if to_date and from_date:
		while (current_date >= from_date):
			r = r + 1
			weekday1 = calendar.day_name[current_date.weekday()]
			x= current_date.strftime('%m-%d-%y')
			current_date_split= x.split("-")
			current_date_string = str(int(current_date_split[0]))+'-'+str(int(current_date_split[1]))+'-'+str(current_date_split[2])
			current_date_string = str(current_date_string)
			result = [current_date_string]
			sheet1.write_rich_string(0,r,weekday1,'\n',current_date_string,format_week)
			# sheet1.write(0, r, current_date,date_format)
			current_date -= timedelta(days=1)
	sheet1.write(1, 0, "Grades",bold)
	sheet1.write(2, 0, "OVERALL HEALTH GRADES",bold)
	col_num1 = 2
	row_num = 0
	for col_num in range(len(columnsw)):
		col_num1 = col_num1 + 1
		sheet1.write(col_num1, row_num, columnsw[col_num])
	current_date = to_date
	i = 0
	while (current_date >= from_date):
		steps_data = steps_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		grades_data = grades_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		sleep_data = sleep_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		food_data = food_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		alcohol_data = alcohol_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		exercise_data = exercise_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		user_input_strong_data = user_input_strong_datewise.get(current_date.strftime("%Y-%m-%d"),None)

		if steps_data and grades_data and exercise_data and food_data and alcohol_data and sleep_data:
			if user_input_strong_data:
				user_input_strong_data = user_input_strong_data.__dict__
			steps_data = steps_data.__dict__
			grades_data = grades_data.__dict__
			sleep_data = sleep_data.__dict__
			exercise_data = exercise_data.__dict__
			alcohol_data = alcohol_data.__dict__
			food_data = food_data.__dict__
			# logic

			row_num += 1
			for i,key in enumerate(columns):
			
				if key != 'non_exercise_steps' and key != 'movement_consistency' and key != 'sleep_per_wearable' and key != 'prcnt_non_processed_food' and key != 'alcohol_week' and key != 'workout' and key != 'overall_gpa_without_penalties':
					if grades_data[key] == 'A':
						sheet1.write(i+3,row_num, grades_data[key],format_green)
					elif grades_data[key] == 'B':
						sheet1.write(i+3,row_num, grades_data[key],format_green)
					elif grades_data[key] == 'C':
						sheet1.write(i+3,row_num, grades_data[key],format_yellow)
					elif grades_data[key] == 'D':
						sheet1.write(i+3,row_num, grades_data[key],format_yellow)
					elif grades_data[key] == 'F':
						sheet1.write(i+3,row_num, grades_data[key],format_red)
					elif grades_data[key] == 'N/A':
						sheet1.write(i+3,row_num, grades_data[key],format1)
					elif i == 10:
						sheet1.write(i+3,row_num, grades_data[key],format_exe)
					elif key == 'sleep_aid_penalty' or key == 'ctrl_subs_penalty' or key == 'smoke_penalty':
						if grades_data[key] == 0:
							sheet1.write(i+3,row_num, 'NO',format1)
						else:	
							sheet1.write(i+3,row_num, 'YES',format_red)
					elif i == 1:
						sheet1.write(i+3,row_num, grades_data[key],format1)
					else:
						sheet1.write(i+3,row_num, 'Not Reported',format1)
				elif i == 3:
					sheet1.write(i+3,row_num, steps_data[key],format)
				elif i == 5 and key == 'movement_consistency' and steps_data[key]:
					sheet1.write(i+3,row_num, ast.literal_eval(steps_data[key])['inactive_hours'],format)
				elif i == 7:
					if user_input_strong_data:
						avg_sleep = user_input_strong_data['sleep_time_excluding_awake_time']
						if avg_sleep and avg_sleep != ":":
							sheet1.write(i+3,row_num, user_input_strong_data['sleep_time_excluding_awake_time'],format1)
						else:
							sheet1.write(i+3,row_num, sleep_data[key],format1)
					else:
						sheet1.write(i+3,row_num, sleep_data[key],format1)
				elif key == 'workout':
					if user_input_strong_data:
						sheet1.write(i+3, row_num, user_input_strong_data[key],format)
					else:
						sheet1.write(i+3, row_num,"Not Reported",format)
				elif i == 12:
					if food_data[key] == '':
						
						sheet1.write(i+3,row_num, '')
					else:
						sheet1.write(i+3,row_num, str(int(food_data[key])) + '%')
				elif i == 14:
					sheet1.write(i+3,row_num, alcohol_data[key],format_exe)
				elif i == 18:
					grade_point = {"A":4,"B":3,"C":2,"D":1,"F":0,"":0}
					# overall_workout_gpa_cal = grades_data['overall_health_gpa']
					# sleep_aid_penalty_cal = grades_data['sleep_aid_penalty']
					# ctrl_subs_penalty_cal = grades_data['ctrl_subs_penalty']
					# smoke_penalty_cal = grades_data['smoke_penalty']
					grades_steps = grades_data['movement_non_exercise_steps_grade']
					grades_consistency = grades_data['movement_consistency_grade']
					grades_sleep = grades_data['avg_sleep_per_night_grade']
					grades_consistency_exe = grades_data['exercise_consistency_grade']
					grades_food = grades_data['prcnt_unprocessed_food_consumed_grade']
					grades_alcohol = grades_data['alcoholic_drink_per_week_grade']
					overall_workout_gpa_without_penalty = (grade_point[grades_steps]+grade_point[grades_consistency]+
					grade_point[grades_sleep]+grade_point[grades_consistency_exe]+grade_point[grades_food]+grade_point[grades_alcohol])/6
					if overall_workout_gpa_without_penalty >= 3:
						sheet1.write(i+3,row_num,overall_workout_gpa_without_penalty,format_green_overall)
					elif overall_workout_gpa_without_penalty >= 1 and overall_workout_gpa_without_penalty < 3:
						sheet1.write(i+3,row_num,overall_workout_gpa_without_penalty,format_yellow_overall)
					elif overall_workout_gpa_without_penalty < 1:
						sheet1.write(i+3,row_num,overall_workout_gpa_without_penalty,format_red_overall)
					# overall_workout_gpa_without_penalty = overall_workout_gpa_cal+sleep_aid_penalty_cal+ctrl_subs_penalty_cal+smoke_penalty_cal
					# sheet1.write(i+3,row_num,overall_workout_gpa_without_penalty,format1)
				else:
					sheet1.write(i+3,row_num,'Not Reported')
			for i,key in enumerate(colunn_work):
				if user_input_strong_data:
					sheet1.write(22,row_num,"Yes")
				else:
					sheet1.write(22,row_num,"No",format_red)
		else:
			row_num += 1
			sheet1.write(i+3,row_num, '')
		current_date -= timedelta(days=1)

	# columnsg2 = ['Resting Heart Rate','Stress Level','Did you Stand for 3 hours or more above and beyond your exercise yesterday?']
	# col = ['sleep_resting_hr_last_night','stress_level','stand_for_three_hours']
	# sheet2.write(21, 0, "NOT GRADED CATEGORIES",bold)
	# col_num2 = 21
	# num_10 = row_num
	# len_gra = len(rows_of_grades)
	# for col_num in range(len(columnsg2)):
	# 	 col_num2 = col_num2 + 1
	# 	 sheet2.write(col_num2,row_num - num_10, columnsg2[col_num])

	# current_date = to_date
	# while (current_date >= from_date):
	# 	options_data = options_datewise.get(current_date.strftime("%Y-%m-%d"),None)
	# 	exercise_data = exercise_datewise.get(current_date.strftime("%Y-%m-%d"),None)
	# 	if options_data and exercise_data:
	# 		options_data = options_data.__dict__
	# 		exercise_data = exercise_data.__dict__
	# 		# logic
	# 		row_num += 1
	# 		for i, key in enumerate(col):
	# 			if key == 'stand_for_three_hours':
	# 				sheet2.write(col_num2+i-2, row_num - num_10, options_data[key],format)
	# 			else:
	# 				sheet2.write(col_num2+i-2, row_num - num_10, exercise_data[key],format)
	# 	else:
	
	# 		row_num += 1
	# 		sheet2.write(col_num2+i-2, row_num - num_10, '')
	# 	current_date -= timedelta(days=1)
	
	# sheet2.write(26, 0, "PERFORMANCE ASSESSMENT",bold)
	# columnsg3 = ['Overall Workout Grade ','Overall Workout Score (points)','Workout Duration Grade','Workout Duration'
	# ,'Workout Effort Level Grade','Workout Effort Level','Average Exercise Heart Rate Grade ','Average Exercise Heart Rate'
	# ,'Heart Rate Recovery (HRR) - time to 99','Heart Rate Recovery (HRR) - heart beats lowered in the first minute '
	# ,'VO2 Max','Floors Climbed ']
	# columnsg4 = ['overall_workout_grade','overall_workout_gpa','workout_duration_grade','workout_duration',
	# 'workout_effortlvl_grade','workout_effortlvl_gpa','avg_exercise_hr_grade','avg_exercise_hr_gpa','time_to_99',
	# 'lowest_hr_first_minute','vo2_max','floor_climed']
	# col_num2 = 26
	# len_gra1 = len(rows_of_grades) + len(exec1) 
	# num_1 = row_num
	# for col_num in range(len(columnsg3)):
	# 	 col_num2 = col_num2 + 1
	# 	 sheet2.write(col_num2,row_num - num_1, columnsg3[col_num])
	# l2 = 26
	# num_2 = row_num

	# current_date = to_date
	# while (current_date >= from_date):
	# 	options_user_data = options_user_input_datewise.get(current_date.strftime("%Y-%m-%d"),None)
	# 	exercise_data = exercise_datewise.get(current_date.strftime("%Y-%m-%d"),None)
	# 	grades_data = grades_datewise.get(current_date.strftime("%Y-%m-%d"),None)
	# 	steps_data = steps_datewise.get(current_date.strftime("%Y-%m-%d"),None)
	# 	if options_user_data and exercise_data and grades_data and steps_data:
	# 		options_user_data = options_user_data.__dict__
	# 		exercise_data = exercise_data.__dict__
	# 		grades_data = grades_data.__dict__
	# 		steps_data = steps_data.__dict__
	# 		# logic
		
	# 		row_num += 1
	# 		for i, key in enumerate(columnsg4):
	# 			if key != 'workout_duration' and key != 'floor_climed' and key != 'vo2_max' and key != 'lowest_hr_first_minute' and key != 'time_to_99':
	# 				if grades_data[key] == 'A':
	# 					sheet2.write(l2+i+1,row_num-num_2, grades_data[key],format_green)
	# 				elif grades_data[key] == 'B':
	# 					sheet2.write(l2+i+1,row_num-num_2, grades_data[key],format_green)
	# 				elif grades_data[key] == 'C':
	# 					sheet2.write(l2+i+1,row_num-num_2, grades_data[key],format_yellow)
	# 				elif grades_data[key] == 'D':
	# 					sheet2.write(l2+i+1,row_num-num_2, grades_data[key],format_yellow)
	# 				elif grades_data[key] == 'F':
	# 					sheet2.write(l2+i+1,row_num-num_2, grades_data[key],format_red)
	# 				elif grades_data[key] == 'N/A':
	# 					sheet2.write(l2+i+1,row_num-num_2, grades_data[key],format1)
	# 				elif grades_data[key] == '':
	# 					sheet2.write(l2+i+1,row_num-num_2, '',format1)
	# 				else:
	# 					sheet2.write(l2+i+1,row_num-num_2,grades_data[key] ,format1)

	# 			elif key == 'workout_duration':
	# 				sheet2.write(l2+i+1, row_num-num_2, exercise_data[key],format)
	# 			elif key == 'floor_climed':
	# 				sheet2.write(l2+i+1, row_num-num_2, steps_data[key],format)
	# 			elif key == 'vo2_max':
	# 				sheet2.write(l2+i+1, row_num-num_2, exercise_data[key],format)
	# 			elif key == 'lowest_hr_first_minute':
	# 				sheet2.write(l2+i+1, row_num-num_2, options_user_data[key],format)
	# 			elif key == 'time_to_99':
	# 				sheet2.write(l2+i+1, row_num-num_2, options_user_data[key],format)
	# 			else:
	# 				sheet2.write(l2+i+1,row_num-num_2, 'YES',format_red)
	# 	else:

	# 		row_num += 1
	# 		sheet2.write(col_num2+i-2, row_num - num_10, '')
	# 	current_date -= timedelta(days=1)



	#Swim Stats sheet
	sheet7.set_landscape()
	sheet7.repeat_rows(0)
	sheet7.repeat_columns(0)
	sheet7.set_row(0,30)
	columns = ['pace_per_100_yard', 'total_strokes']
	current_date = to_date
	r = 0
	if to_date and from_date:
		while (current_date >= from_date):
			r = r + 1
			weekday1 = calendar.day_name[current_date.weekday()]
			x= current_date.strftime('%m-%d-%y')
			current_date_split= x.split("-")
			current_date_string = str(int(current_date_split[0]))+'-'+str(int(current_date_split[1]))+'-'+str(current_date_split[2])
			current_date_string = str(current_date_string)
			sheet7.write_rich_string(0,r,weekday1,'\n',current_date_string,format_week)
			# sheet7.write(0, r, current_date,date_format)
			current_date -= timedelta(days=1)
	sheet7.write(0, 0, "Swim Stats",bold)
	col_num1 = 1
	row_num = 0
	for col_num in range(len(columns1W)):
		col_num1 = col_num1 + 1
		sheet7.write(col_num1, row_num, columns1W[col_num])



	current_date = to_date
	for row in swim_qs.values():
		
		while (current_date >= from_date):
			data = swim_datewise.get(current_date.strftime("%Y-%m-%d"),None)
			if data:
				# logic
				row_num += 1
				for i,key in enumerate(columns):
					sheet7.write(i + 2, row_num, row[key],format)
			else:
				row_num += 1
				sheet7.write(i + 2, row_num, '')
			current_date -= timedelta(days=1)
	# Bike stats sheet
	sheet8.set_landscape()
	sheet8.repeat_rows(0)
	sheet8.repeat_columns(0)
	sheet8.set_row(0,30)
	columns = ['avg_speed', 'avg_power','avg_speed_per_mile','avg_cadence']
	current_date = to_date
	r = 0
	if to_date and from_date:
		while (current_date >= from_date):
			r = r + 1
			weekday1 = calendar.day_name[current_date.weekday()]
			x= current_date.strftime('%m-%d-%y')
			current_date_split= x.split("-")
			current_date_string = str(int(current_date_split[0]))+'-'+str(int(current_date_split[1]))+'-'+str(current_date_split[2])
			current_date_string = str(current_date_string)
			sheet8.write_rich_string(0,r,weekday1,'\n',current_date_string,format_week)
			# sheet8.write(0, r, current_date,date_format)
			current_date -= timedelta(days=1)
	sheet8.write(0, 0, "Bike Stats",bold)
	col_num1 = 1
	row_num = 0
	for col_num in range(len(columns3W)):
		col_num1 = col_num1 + 1
		sheet8.write(col_num1, row_num, columns3W[col_num])

	
	current_date = to_date
	for row in bike_qs.values():

		while (current_date >= from_date):
			# logic
			data = bike_datewise.get(current_date.strftime("%Y-%m-%d"),None)
			if data:
				row_num += 1
				for i,key in enumerate(columns):
					sheet8.write(i + 2, row_num, row[key],format)
			else:
				row_num += 1
				sheet8.write(i + 2, row_num, '')
			current_date -= timedelta(days=1)

	# steps stats sheet
	sheet2.set_landscape()
	sheet2.repeat_rows(0)
	sheet2.repeat_columns(0)
	sheet2.set_row(0,30)
	columns = ['movement_consistency','non_exercise_steps', 'exercise_steps', 'total_steps', 'floor_climed']
	current_date = to_date
	r = 0
	if to_date and from_date:
		while (current_date >= from_date):
			r = r + 1
			weekday1 = calendar.day_name[current_date.weekday()]
			x= current_date.strftime('%m-%d-%y')
			current_date_split= x.split("-")
			current_date_string = str(int(current_date_split[0]))+'-'+str(int(current_date_split[1]))+'-'+str(current_date_split[2])
			current_date_string = str(current_date_string)
			sheet2.write_rich_string(0,r,weekday1,'\n',current_date_string,format_week)
			# sheet2.write(0, r, current_date,date_format)
			current_date -= timedelta(days=1)
	sheet2.write(0, 0, "Steps",bold)
	col_num1 = 1
	row_num = 0
	for col_num in range(len(columns4W)):
		col_num1 = col_num1 + 1
		sheet2.write(col_num1, row_num, columns4W[col_num])



	current_date = to_date

	while (current_date >= from_date):
		steps_data = steps_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		grades_data = grades_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		if steps_data and grades_data:
			steps_data = steps_data.__dict__
			grades_data = grades_data.__dict__
			# logic

			row_num += 1
			for i,key in enumerate(columns4):
				if i == 1 and grades_data['movement_non_exercise_steps_grade'] == 'A':
					sheet2.write(i + 2, row_num, steps_data[key], format_green)
				elif i == 1 and grades_data['movement_non_exercise_steps_grade'] == 'B':
					sheet2.write(i + 2, row_num,steps_data[key], format_green)
				elif i == 1 and grades_data['movement_non_exercise_steps_grade'] == 'C':
					sheet2.write(i + 2, row_num, steps_data[key], format_yellow)
				elif i == 1 and grades_data['movement_non_exercise_steps_grade'] == 'D':
					sheet2.write(i + 2, row_num, steps_data[key], format_yellow)
				elif i == 1 and grades_data['movement_non_exercise_steps_grade'] == 'F':
					sheet2.write(i + 2, row_num, steps_data[key], format_red)
				elif i == 0 and grades_data['movement_consistency_grade'] == 'A' and key == 'movement_consistency' and steps_data[key]:
					sheet2.write(i + 2, row_num, ast.literal_eval(steps_data[key])['inactive_hours'], format_green)
				elif i == 0 and grades_data['movement_consistency_grade'] == 'B' and key == 'movement_consistency' and steps_data[key]:
					sheet2.write(i + 2, row_num, ast.literal_eval(steps_data[key])['inactive_hours'], format_green)
				elif i == 0 and grades_data['movement_consistency_grade'] == 'C' and key == 'movement_consistency' and steps_data[key]:
					sheet2.write(i + 2, row_num, ast.literal_eval(steps_data[key])['inactive_hours'], format_yellow)
				elif i == 0 and grades_data['movement_consistency_grade'] == 'D' and key == 'movement_consistency' and steps_data[key]:
					sheet2.write(i + 2, row_num, ast.literal_eval(steps_data[key])['inactive_hours'], format_yellow)
				elif i == 0 and grades_data['movement_consistency_grade'] == 'F' and key == 'movement_consistency' and steps_data[key]:
					sheet2.write(i + 2, row_num,ast.literal_eval(steps_data[key])['inactive_hours'], format_red)
				else:
					sheet2.write(i + 2, row_num, steps_data[key], format)
		else:
			row_num += 1
			sheet2.write(i + 2, row_num,'')
		current_date -= timedelta(days=1)

	# sleep stats sheet
	sheet3.set_landscape()
	sheet3.repeat_rows(0)
	sheet3.repeat_columns(0)
	sheet3.set_row(0,30)
	columns = ['sleep_per_user_input','sleep_comments',  'sleep_aid','sleep_per_wearable', 'sleep_bed_time', 'sleep_awake_time',
			   'deep_sleep','light_sleep','awake_time']
	current_date = to_date
	r = 0
	if to_date and from_date:
		while (current_date >= from_date):
			r = r + 1
			weekday1 = calendar.day_name[current_date.weekday()]
			x= current_date.strftime('%m-%d-%y')
			current_date_split= x.split("-")
			current_date_string = str(int(current_date_split[0]))+'-'+str(int(current_date_split[1]))+'-'+str(current_date_split[2])
			current_date_string = str(current_date_string)
			sheet3.write_rich_string(0,r,weekday1,'\n',current_date_string,format_week)
			# sheet3.write(0, r, current_date,date_format)
			current_date -= timedelta(days=1)
	sheet3.write(0, 0, "Sleep",bold)
	col_num1 = 1
	row_num = 0
	for col_num in range(len(columns5W)):
		col_num1 = col_num1 + 1
		sheet3.write(col_num1, row_num, columns5W[col_num])

	format2 = book.add_format()
	format2.set_align('top')
	format2.set_text_wrap()

	format2.set_shrink()
	# wrap = book.add_format({'text_wrap': True})
	sheet3.set_row(3, 150)
	

	current_date = to_date
		
	while (current_date >= from_date):
		sleep_data = sleep_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		exercise_data = exercise_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		grades_data = grades_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		user_input_strong_data = user_input_strong_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		if sleep_data and exercise_data and grades_data:
			if user_input_strong_data:
				user_input_strong_data = user_input_strong_data.__dict__
			sleep_data = sleep_data.__dict__
			grades_data = grades_data.__dict__
			exercise_data = exercise_data.__dict__
			# logic
			row_num += 1
			for i, key in enumerate(columns5):
				if user_input_strong_data:
					
					if i == 0 and grades_data['avg_sleep_per_night_grade'] == 'A':
						sheet3.write(i + 2, row_num, user_input_strong_data['sleep_time_excluding_awake_time'], format_green)
					elif i == 0 and grades_data['avg_sleep_per_night_grade'] == 'B':
						sheet3.write(i + 2, row_num, user_input_strong_data['sleep_time_excluding_awake_time'], format_green)
					elif i == 0 and grades_data['avg_sleep_per_night_grade'] == 'C':
						sheet3.write(i + 2, row_num, user_input_strong_data['sleep_time_excluding_awake_time'], format_yellow)
					elif i == 0 and grades_data['avg_sleep_per_night_grade'] == 'D':
						sheet3.write(i + 2, row_num,user_input_strong_data['sleep_time_excluding_awake_time'], format_yellow)
					elif i == 0 and grades_data['avg_sleep_per_night_grade'] == 'F':
						sheet3.write(i + 2, row_num,user_input_strong_data['sleep_time_excluding_awake_time'], format_red)
				elif i == 1:
					sheet3.write(i + 2, row_num,sleep_data[key], format2)
				elif i == 3:
					if exercise_data[key] >= 76:
						sheet3.write(i + 2, row_num, exercise_data[key], format_red)
					if exercise_data[key] >= 63 and exercise_data[key] <= 75:
						sheet3.write(i + 2, row_num, exercise_data[key], format_yellow)
					if exercise_data[key] > 30 and exercise_data[key] <= 62:
						sheet3.write(i + 2, row_num, exercise_data[key], format_green)
					if exercise_data[key] <= 30:
						sheet3.write(i + 2, row_num, exercise_data[key], format_red)
	
			
				if i != 0 and i != 3:
					sheet3.write(i + 2, row_num, sleep_data[key], format)
		else:
			row_num += 1
			sheet3.write(i + 2, row_num, '')
		current_date -= timedelta(days=1)
	# Food sheet
	sheet4.set_landscape()
	sheet4.repeat_rows(0)
	sheet4.repeat_columns(0)
	sheet4.set_row(0,30)
	columns = ['prcnt_non_processed_food','processed_food','non_processed_food', 'diet_type']
	current_date = to_date
	r = 0
	if to_date and from_date:
		while (current_date >= from_date):
			r = r + 1
			weekday1 = calendar.day_name[current_date.weekday()]
			x= current_date.strftime('%m-%d-%y')
			current_date_split= x.split("-")
			current_date_string = str(int(current_date_split[0]))+'-'+str(int(current_date_split[1]))+'-'+str(current_date_split[2])
			current_date_string = str(current_date_string)
			sheet4.write_rich_string(0,r,weekday1,'\n',current_date_string,format_week)
			# sheet4.write(0, r, current_date,date_format)
			current_date -= timedelta(days=1)
	sheet4.write(0, 0, "Food",bold)
	col_num1 = 1
	row_num = 0
	for col_num in range(len(columns6W)):
		col_num1 = col_num1 + 1
		sheet4.write(col_num1, row_num, columns6W[col_num])

	format2 = book.add_format()
	format2.set_align('fill')



	current_date = to_date
	while (current_date >= from_date):
		food_data = food_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		grades_data = grades_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		if food_data and grades_data:
			food_data = food_data.__dict__
			grades_data = grades_data.__dict__
			# logic
			row_num += 1
			for i, key in enumerate(columns):
				if grades_data['prcnt_unprocessed_food_consumed_grade'] == 'A' and i == 0:
					sheet4.write(i + 2, row_num,str(int(food_data[key])) + '%' ,format_green)
				elif grades_data['prcnt_unprocessed_food_consumed_grade'] == 'B' and i == 0:
					sheet4.write(i + 2, row_num, str(int(food_data[key])) + '%' ,format_green)
				elif grades_data['prcnt_unprocessed_food_consumed_grade'] == 'C' and i == 0:
					sheet4.write(i + 2, row_num,str(int(food_data[key])) + '%' ,format_yellow)
				elif grades_data['prcnt_unprocessed_food_consumed_grade'] == 'D' and i == 0:
					sheet4.write(i + 2, row_num,str(int(food_data[key])) + '%' ,format_yellow)
				elif grades_data['prcnt_unprocessed_food_consumed_grade'] == 'F' and i == 0:
					sheet4.write(i + 2, row_num,str(int(food_data[key])) + '%' ,format_red)
				elif grades_data['prcnt_unprocessed_food_consumed_grade'] == '':
					sheet4.write(i + 2, row_num,'Not Reported',)
				else:
					sheet4.write(i + 2, row_num, food_data[key], format)
		else:
			
			row_num += 1
			sheet4.write(i + 2, row_num, '')
		current_date -= timedelta(days=1)
	# Alcohol sheet
	sheet5.set_landscape()
	sheet5.repeat_rows(0)
	sheet5.repeat_columns(0)
	sheet5.set_row(0,30)
	columns = ['alcohol_day', 'alcohol_week']
	current_date = to_date
	r = 0
	if to_date and from_date:
		while (current_date >= from_date):
			r = r + 1
			weekday1 = calendar.day_name[current_date.weekday()]
			x= current_date.strftime('%m-%d-%y')
			current_date_split= x.split("-")
			current_date_string = str(int(current_date_split[0]))+'-'+str(int(current_date_split[1]))+'-'+str(current_date_split[2])
			current_date_string = str(current_date_string)
			sheet5.write_rich_string(0,r,weekday1,'\n',current_date_string,format_week)
			# sheet5.write(0, r, current_date,date_format)
			current_date -= timedelta(days=1)
	sheet5.write(0, 0, "Alcohol",bold)
	col_num1 = 1
	row_num = 0
	for col_num in range(len(columns7W)):
		col_num1 = col_num1 + 1
		sheet5.write(col_num1, row_num, columns7W[col_num])



	current_date = to_date
	while (current_date >= from_date):
		alcohol_data = alcohol_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		grades_data = grades_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		if alcohol_data and grades_data:
			alcohol_data = alcohol_data.__dict__
			grades_data = grades_data.__dict__
			# logic
			row_num += 1
			for i, key in enumerate(columns):
				# float_val = map
				# x = float(alcohol_data[key])
				if i == 1 and grades_data['alcoholic_drink_per_week_grade'] == 'A':
					sheet5.write(i + 2, row_num, alcohol_data[key], format_green_a)
				elif i == 1 and grades_data['alcoholic_drink_per_week_grade'] == 'B':
					sheet5.write(i + 2, row_num, alcohol_data[key], format_green_a)
				elif i == 1 and grades_data['alcoholic_drink_per_week_grade'] == 'C':
					sheet5.write(i + 2, row_num, alcohol_data[key], format_yellow_a)
				elif i == 1 and grades_data['alcoholic_drink_per_week_grade'] == 'D':
					sheet5.write(i + 2, row_num, alcohol_data[key], format_yellow_a)
				elif i == 1 and grades_data['alcoholic_drink_per_week_grade'] == 'F':
					sheet5.write(i + 2, row_num, alcohol_data[key], format_red_a)
				else:
					if alcohol_data[key] == '':
						sheet5.write(i + 2, row_num, 'Not Reported',format_exe)
					elif alcohol_data[key] == '20+':
						sheet5.write(i + 2, row_num, '20+')
					else:
						sheet5.write(i + 2, row_num, float(str(alcohol_data[key])),format_exe)
		else:
		
			row_num += 1
			sheet5.write(i + 2, row_num, '')
		current_date -= timedelta(days=1)

	# Exercise Reporting

	sheet6.set_landscape()
	sheet6.repeat_rows(0)
	sheet6.repeat_columns(0)
	sheet6.set_row(0,30)
	columns = ["workout_easy_hard","workout_type","workout_time", "workout_location","workout_duration","maximum_elevation_workout","minutes_walked_before_workout",
	"distance_run","distance_bike","distance_swim","distance_other","pace","avg_heartrate","avg_heartrate","avg_heartrate",
	"elevation_gain","elevation_loss","effort_level","dew_point","temperature","humidity",
	"temperature_feels_like","wind","hrr_time_to_99","hrr_starting_point","hrr_beats_lowered_first_minute","resting_hr_last_night","vo2_max","running_cadence",
	"nose_breath_prcnt_workout","water_consumed_workout","chia_seeds_consumed_workout","fast_before_workout","pain","pain_area","stress_level","sick","drug_consumed",
	"drug","medication","smoke_substance","exercise_fifteen_more","workout_elapsed_time","timewatch_paused_workout","exercise_consistency",
	"heartrate_variability_stress","fitness_age","workout_comment"]
	columns8w = ['Workout Easy Hard','Workout Type', 'Workout Time','Workout Location','Workout Duration (hh:mm:ss)','Maximum Elevation Workout','Minutes Walked Before Workout','Distance (In Miles) - Run', 
	'Distance (in Miles) - Bike', 'Distance (in yards) - Swim', 'Distance (in Miles) - Other','Pace (minutes:seconds) (Running)','Average Heartrate RUNNING','Average Heartrate ELLIPTICAL','Average Heartrate OTHER','Elevation Gain(feet)','Elevation Loss(feet)', 
	'Effort Level','Dew Point (in °F)','Temperature (in °F)','Humidity (in %)',  'Temperature Feels Like (in °F)', 'Wind (in miles per hour)','HRR - Time to 99 (mm:ss)','HRR Start Point',  'HRR Beats Lowered','Sleep Resting Hr Last Night',
	'Vo2 Max','Running Cadence','Percent Breath through Nose During Workout','Water Consumed during Workout','Chia Seeds consumed during Workout','Fast Before Workout', 'Pain','Pain Area','Stress Level','Sick ', 'Drug Consumed',
	'Drug','Medication','Smoke Substance', 'Exercise Fifteen More','Workout Elapsed Time','TimeWatch Paused Workout','Exercise Consistency','Heart Rate Variability Stress (Garmin)','Fitness Age','Workout Comment']
	
	current_date = to_date
	r = 0
	if to_date and from_date:
		while (current_date >= from_date):
			r = r + 1
			weekday1 = calendar.day_name[current_date.weekday()]
			x= current_date.strftime('%m-%d-%y')
			current_date_split= x.split("-")
			current_date_string = str(int(current_date_split[0]))+'-'+str(int(current_date_split[1]))+'-'+str(current_date_split[2])
			current_date_string = str(current_date_string)
			sheet6.write_rich_string(0,r,weekday1,'\n',current_date_string,format_week)
			# sheet6.write(0, r, current_date,date_format)
			current_date -= timedelta(days=1)
	sheet6.write(0, 0, "Exercise Reporting",bold)
	col_num1 = 1
	row_num = 0
	for col_num in range(len(columns8w)):
		col_num1 = col_num1 + 1
		sheet6.write(col_num1, row_num, columns8w[col_num])

	current_date = to_date
	# for row in exercise_qs.values():
		# print (row)
	while (current_date >= from_date):
		# logic
		data = exercise_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		if data:
			data = data.__dict__
			# print(data)
			row_num += 1
			for i,key in enumerate(columns):
				avg_heart_rate_string = data['avg_heartrate']
				json2_data = json.loads(avg_heart_rate_string)
				
				if i == 12:
					if 'RUNNING' in json2_data:
					 	sheet6.write(i+2,row_num,json2_data['RUNNING'],format)
					else:
					 	sheet6.write(i+2,row_num,"",format)
				elif i == 13:
					if 'ELLIPTICAL' in json2_data:
					 	sheet6.write(i+2,row_num,json2_data['ELLIPTICAL'],format)
					else:
					 	sheet6.write(i+2,row_num,"",format)
				elif i == 14:
					if 'OTHER' in json2_data:
					 	sheet6.write(i+2,row_num,json2_data['OTHER'],format)
				elif data[key] == None:
					sheet6.write(i + 2, row_num,'Not Reported')
				elif key != 'avg_heartrate':
					sheet6.write(i + 2, row_num,data[key],format)


		else:
			row_num += 1
			sheet6.write(i + 2, row_num, '')
		current_date -= timedelta(days=1)
	
	#movement consistenct
	sheet11 = book.add_worksheet('Movement Consistency')
	sheet11.set_landscape()
	sheet11.fit_to_pages(1, 1)
	sheet11.set_zoom(73)
	sheet11.write(0,0,"Movement Consistency Historical Data",bold)
	sheet11.write(0,10,"Sleeping",format_orange)
	sheet11.write(0,11,"Active",format_green)
	sheet11.write(0,12,"Inactive",format_red_con)
	sheet11.write(0,13,"Strength",format_purple)
	sheet11.write(2,0,"Hour")
	sheet11.write(3,0,"Date",bold)
	format2 = book.add_format({'bold':True})
	format2.set_align('bottom')
	format2.set_text_wrap()
	format3 = book.add_format({'bold':True,'align':'center'})
	format3.set_align('bottom')
	format3.set_text_wrap()
	format4 = book.add_format({'bold':True})
	format4.set_num_format("0%") 
	sheet11.set_column('D:AA',8)
	sheet11.freeze_panes(4,3)
	sheet11.set_column(1,1,15)
	sheet11.write(5,0,'% of Days User Gets 300  in the hour*',bold)
	# format2.set_shrink()
	sheet11.write(3,1,"Daily Movement Consistency Score",format3)
	hours_range = ["Total Daily Steps","12:00 - 12:59 AM","01:00 - 01:59 AM","02:00 - 02:59 AM","03:00 - 03:59 AM","04:00 - 04:59 AM",
	"05:00 - 05:59 AM","06:00 - 06:59 AM","07:00 - 07:59 AM","08:00 - 08:59 AM","09:00 - 09:59 AM","10:00 - 10:59 AM","11:00 - 11:59 AM",
	"12:00 - 12:59 PM","01:00 - 01:59 PM","02:00 - 02:59 PM","03:00 - 03:59 PM","04:00 - 04:59 PM","05:00 - 05:59 PM",
	"06:00 - 06:59 PM","07:00 - 07:59 PM","08:00 - 08:59 PM","09:00 - 09:59 PM","10:00 - 10:59 PM","11:00 - 11:59 PM","Sleeping Hours",
	"Active Hours","Inactive Hours","Strength Hours"]
	hours_range1 = ["total_steps","12:00 AM to 12:59 AM","01:00 AM to 01:59 AM","02:00 AM to 02:59 AM","03:00 AM to 03:59 AM","04:00 AM to 04:59 AM",
	"05:00 AM to 05:59 AM","06:00 AM to 06:59 AM","07:00 AM to 07:59 AM","08:00 AM to 08:59 AM","09:00 AM to 09:59 AM","10:00 AM to 10:59 AM","11:00 AM to 11:59 AM",
	"12:00 PM to 12:59 PM","01:00 PM to 01:59 PM","02:00 PM to 02:59 PM","03:00 PM to 03:59 PM","04:00 PM to 04:59 PM","05:00 PM to 05:59 PM",
	"06:00 PM to 06:59 PM","07:00 PM to 07:59 PM","08:00 PM to 08:59 PM","09:00 PM to 09:59 PM","10:00 PM to 10:59 PM","11:00 PM to 11:59 PM","sleeping_hours",
	"active_hours","inactive_hours"]
	days_count = {"12:00 AM to 12:59 AM":0,"01:00 AM to 01:59 AM":0,"02:00 AM to 02:59 AM":0,"03:00 AM to 03:59 AM":0,"04:00 AM to 04:59 AM":0,
	"05:00 AM to 05:59 AM":0,"06:00 AM to 06:59 AM":0,"07:00 AM to 07:59 AM":0,"08:00 AM to 08:59 AM":0,"09:00 AM to 09:59 AM":0,"10:00 AM to 10:59 AM":0,"11:00 AM to 11:59 AM":0,
	"12:00 PM to 12:59 PM":0,"01:00 PM to 01:59 PM":0,"02:00 PM to 02:59 PM":0,"03:00 PM to 03:59 PM":0,"04:00 PM to 04:59 PM":0,"05:00 PM to 05:59 PM":0,
	"06:00 PM to 06:59 PM":0,"07:00 PM to 07:59 PM":0,"08:00 PM to 08:59 PM":0,"09:00 PM to 09:59 PM":0,"10:00 PM to 10:59 PM":0,"11:00 PM to 11:59 PM":0}
	columns = ['movement_consistency']
	current_date = to_date
	r = 6
	# ?from_date=01-31-2018&to_date=01-05-2018
	total_days = (to_date-from_date).days+1

	if to_date and from_date:
		while (current_date >= from_date):
			r = r + 1
			sheet11.write(r,0,current_date,date_format)
			current_date -= timedelta(days = 1)
	sheet11.set_row(3,45)
	col_num = 2
	start_num = 12
	start_digit =':01'
	end_digit = ':59'
	for hour in range(1,25,1):
		col_num += 1
		sheet11.write(2,col_num,hour)
	col_num1 = 1
	for col_num in range(len(hours_range)):
		col_num1 += 1
		sheet11.write(3,col_num1,hours_range[col_num],format2)
	current_date = to_date
	row_num = 4
	row = 6
	row_per = 5
	col = 2
	while (current_date >= from_date):
		steps_data = steps_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		grades_data = grades_datewise.get(current_date.strftime("%Y-%m-%d"),None)
		if steps_data:
			steps_data = steps_data.__dict__
			grades_data = grades_data.__dict__
			# logic
			row += 1
			for i,key in enumerate(columns4):
				
				if i == 0 and grades_data['movement_consistency_grade'] == 'A' and key == 'movement_consistency' and steps_data[key]:
					sheet11.write(row,col-1,ast.literal_eval(steps_data[key])['inactive_hours'], format_green)
				elif i == 0 and grades_data['movement_consistency_grade'] == 'B' and key == 'movement_consistency' and steps_data[key]:
					sheet11.write(row,col-1, ast.literal_eval(steps_data[key])['inactive_hours'], format_green)
				elif i == 0 and grades_data['movement_consistency_grade'] == 'C' and key == 'movement_consistency' and steps_data[key]:
					sheet11.write(row,col-1, ast.literal_eval(steps_data[key])['inactive_hours'], format_yellow)
				elif i == 0 and grades_data['movement_consistency_grade'] == 'D' and key == 'movement_consistency' and steps_data[key]:
					sheet11.write(row,col-1, ast.literal_eval(steps_data[key])['inactive_hours'], format_yellow)
				elif i == 0 and grades_data['movement_consistency_grade'] == 'F' and key == 'movement_consistency' and steps_data[key]:
					sheet11.write(row,col-1,ast.literal_eval(steps_data[key])['inactive_hours'], format_red_con)
				# else:
				# 	sheet11.write(i + 2, row_num, steps_data[key], format)
			for x,key in enumerate(columns):
				steps_string = steps_data['movement_consistency']
				if steps_string:
					json1_data = json.loads(steps_string)
					sheet11.write(row,col+x,json1_data['total_steps'],format)
					# sheet11.write(row, col, ast.literal_eval(steps_data[key])['inactive_hours'])
					# sheet11.write(row,col+x+1,json1_data['12:00 AM to 12:59 AM']['steps'])
					if json1_data['12:00 AM to 12:59 AM']["status"] == "sleeping":
						sheet11.write(row,col+x+1,json1_data['12:00 AM to 12:59 AM']['steps'],format_orange)
						if json1_data['12:00 AM to 12:59 AM']['steps'] >= 300:
							days_count['12:00 AM to 12:59 AM'] += 1
					elif json1_data['12:00 AM to 12:59 AM']["status"] == "active":
						sheet11.write(row,col+x+1,json1_data['12:00 AM to 12:59 AM']['steps'],format_green)
						if json1_data['12:00 AM to 12:59 AM']['steps'] >= 300:
							days_count['12:00 AM to 12:59 AM'] += 1
					elif json1_data['12:00 AM to 12:59 AM']["status"] == "inactive":
						sheet11.write(row,col+x+1,json1_data['12:00 AM to 12:59 AM']['steps'],format_red_con)
						if json1_data['12:00 AM to 12:59 AM']['steps'] >= 300:
							days_count['12:00 AM to 12:59 AM'] += 1
					else:
						sheet11.write(row,col+x+1,json1_data['12:00 AM to 12:59 AM']['steps'],format_purple)
					if json1_data['01:00 AM to 01:59 AM']["status"] == "sleeping":
						sheet11.write(row,col+x+2,json1_data['01:00 AM to 01:59 AM']['steps'],format_orange)
						if json1_data['01:00 AM to 01:59 AM']['steps'] >= 300:
							days_count['01:00 AM to 01:59 AM'] += 1
					elif json1_data['01:00 AM to 01:59 AM']["status"] == "active":
						sheet11.write(row,col+x+2,json1_data['01:00 AM to 01:59 AM']['steps'],format_green)
						if json1_data['01:00 AM to 01:59 AM']['steps'] >= 300:
							days_count['01:00 AM to 01:59 AM'] += 1
					elif json1_data['01:00 AM to 01:59 AM']["status"] == "inactive":
						sheet11.write(row,col+x+2,json1_data['01:00 AM to 01:59 AM']['steps'],format_red_con)

					else:
						sheet11.write(row,col+x+2,json1_data['01:00 AM to 01:59 AM']['steps'],format_purple)

					if json1_data['02:00 AM to 02:59 AM']["status"] == "sleeping":
						sheet11.write(row,col+x+3,json1_data['02:00 AM to 02:59 AM']['steps'],format_orange)
						if json1_data['02:00 AM to 02:59 AM']['steps'] >= 300:
							days_count['02:00 AM to 02:59 AM'] += 1
					elif json1_data['02:00 AM to 02:59 AM']["status"] == "active":
						sheet11.write(row,col+x+3,json1_data['02:00 AM to 02:59 AM']['steps'],format_green)
						if json1_data['02:00 AM to 02:59 AM']['steps'] >= 300:
							days_count['02:00 AM to 02:59 AM'] += 1
					elif json1_data['02:00 AM to 02:59 AM']["status"] == "inactive":
						sheet11.write(row,col+x+3,json1_data['02:00 AM to 02:59 AM']['steps'],format_red_con)
						if json1_data['02:00 AM to 02:59 AM']['steps'] >= 300:
							days_count['02:00 AM to 02:59 AM'] += 1
					else:
						sheet11.write(row,col+x+3,json1_data['02:00 AM to 02:59 AM']['steps'],format_purple)

					if json1_data['03:00 AM to 03:59 AM']["status"] == "sleeping":
						sheet11.write(row,col+x+4,json1_data['03:00 AM to 03:59 AM']['steps'],format_orange)
						if json1_data['03:00 AM to 03:59 AM']['steps'] >= 300:
							days_count['03:00 AM to 03:59 AM'] += 1
					elif json1_data['03:00 AM to 03:59 AM']["status"] == "active":
						sheet11.write(row,col+x+4,json1_data['03:00 AM to 03:59 AM']['steps'],format_green)
						if json1_data['03:00 AM to 03:59 AM']['steps'] >= 300:
							days_count['03:00 AM to 03:59 AM'] += 1
					elif json1_data['03:00 AM to 03:59 AM']["status"] == "inactive":
						sheet11.write(row,col+x+4,json1_data['03:00 AM to 03:59 AM']['steps'],format_red_con)
						if json1_data['03:00 AM to 03:59 AM']['steps'] >= 300:
							days_count['03:00 AM to 03:59 AM'] += 1
					else:
						sheet11.write(row,col+x+4,json1_data['03:00 AM to 03:59 AM']['steps'],format_purple)

					if json1_data['04:00 AM to 04:59 AM']["status"] == "sleeping":
						sheet11.write(row,col+x+5,json1_data['04:00 AM to 04:59 AM']['steps'],format_orange)
						if json1_data['04:00 AM to 04:59 AM']['steps'] >= 300:
							days_count['04:00 AM to 04:59 AM'] += 1
					elif json1_data['04:00 AM to 04:59 AM']["status"] == "active":
						sheet11.write(row,col+x+5,json1_data['04:00 AM to 04:59 AM']['steps'],format_green)
						if json1_data['04:00 AM to 04:59 AM']['steps'] >= 300:
							days_count['04:00 AM to 04:59 AM'] += 1
					elif json1_data['04:00 AM to 04:59 AM']["status"] == "inactive":
						sheet11.write(row,col+x+5,json1_data['04:00 AM to 04:59 AM']['steps'],format_red_con)
						if json1_data['04:00 AM to 04:59 AM']['steps'] >= 300:
							days_count['04:00 AM to 04:59 AM']+= 1
					else:
						sheet11.write(row,col+x+5,json1_data['04:00 AM to 04:59 AM']['steps'],format_purple)
					#5
					if json1_data['05:00 AM to 05:59 AM']["status"] == "sleeping":
						sheet11.write(row,col+x+6,json1_data['05:00 AM to 05:59 AM']['steps'],format_orange)
						if json1_data['05:00 AM to 05:59 AM']['steps'] >= 300:
							days_count['05:00 AM to 05:59 AM']+= 1
					elif json1_data['05:00 AM to 05:59 AM']["status"] == "active":
						sheet11.write(row,col+x+6,json1_data['05:00 AM to 05:59 AM']['steps'],format_green)
						if json1_data['05:00 AM to 05:59 AM']['steps'] >= 300:
							days_count['05:00 AM to 05:59 AM']+= 1
					elif json1_data['05:00 AM to 05:59 AM']["status"] == "inactive":
						sheet11.write(row,col+x+6,json1_data['05:00 AM to 05:59 AM']['steps'],format_red_con)
						if json1_data['05:00 AM to 05:59 AM']['steps'] >= 300:
							days_count['05:00 AM to 05:59 AM']+= 1
					else:
						sheet11.write(row,col+x+6,json1_data['05:00 AM to 05:59 AM']['steps'],format_purple)
					#6
					if json1_data['06:00 AM to 06:59 AM']["status"] == "sleeping":
						sheet11.write(row,col+x+7,json1_data['06:00 AM to 06:59 AM']['steps'],format_orange)
						if json1_data['06:00 AM to 06:59 AM']['steps'] >= 300:
							days_count['06:00 AM to 06:59 AM']+= 1
					elif json1_data['06:00 AM to 06:59 AM']["status"] == "active":
						sheet11.write(row,col+x+7,json1_data['06:00 AM to 06:59 AM']['steps'],format_green)
						if json1_data['06:00 AM to 06:59 AM']['steps'] >= 300:
							days_count['06:00 AM to 06:59 AM']+= 1
					elif json1_data['06:00 AM to 06:59 AM']["status"] == "inactive":
						sheet11.write(row,col+x+7,json1_data['06:00 AM to 06:59 AM']['steps'],format_red_con)

					else:
						sheet11.write(row,col+x+7,json1_data['06:00 AM to 06:59 AM']['steps'],format_purple)
					#7
					if json1_data['07:00 AM to 07:59 AM']["status"] == "sleeping":
						sheet11.write(row,col+x+8,json1_data['07:00 AM to 07:59 AM']['steps'],format_orange)
						if json1_data['07:00 AM to 07:59 AM']['steps'] >= 300:
							days_count['07:00 AM to 07:59 AM']+= 1
					elif json1_data['07:00 AM to 07:59 AM']["status"] == "active":
						sheet11.write(row,col+x+8,json1_data['07:00 AM to 07:59 AM']['steps'],format_green)
						if json1_data['07:00 AM to 07:59 AM']['steps'] >= 300:
							days_count['07:00 AM to 07:59 AM']+= 1
					elif json1_data['07:00 AM to 07:59 AM']["status"] == "inactive":
						sheet11.write(row,col+x+8,json1_data['07:00 AM to 07:59 AM']['steps'],format_red_con)
					else:
						sheet11.write(row,col+x+8,json1_data['07:00 AM to 07:59 AM']['steps'],format_purple)
					#8
					if json1_data['08:00 AM to 08:59 AM']["status"] == "sleeping":
						sheet11.write(row,col+x+9,json1_data['08:00 AM to 08:59 AM']['steps'],format_orange)
						if json1_data['08:00 AM to 08:59 AM']['steps'] >= 300:
							days_count['08:00 AM to 08:59 AM']+= 1
					elif json1_data['08:00 AM to 08:59 AM']["status"] == "active":
						sheet11.write(row,col+x+9,json1_data['08:00 AM to 08:59 AM']['steps'],format_green)
						if json1_data['08:00 AM to 08:59 AM']['steps'] >= 300:
							days_count['08:00 AM to 08:59 AM']+= 1
					elif json1_data['08:00 AM to 08:59 AM']["status"] == "inactive":
						sheet11.write(row,col+x+9,json1_data['08:00 AM to 08:59 AM']['steps'],format_red_con)
					else:
						sheet11.write(row,col+x+9,json1_data['08:00 AM to 08:59 AM']['steps'],format_purple)
					#9
					if json1_data['09:00 AM to 09:59 AM']["status"] == "sleeping":
						sheet11.write(row,col+x+10,json1_data['09:00 AM to 09:59 AM']['steps'],format_orange)
						if json1_data['09:00 AM to 09:59 AM']['steps'] >= 300:
							days_count['09:00 AM to 09:59 AM']+= 1
					elif json1_data['09:00 AM to 09:59 AM']["status"] == "active":
						sheet11.write(row,col+x+10,json1_data['09:00 AM to 09:59 AM']['steps'],format_green)
						if json1_data['09:00 AM to 09:59 AM']['steps'] >= 300:
							days_count['09:00 AM to 09:59 AM']+= 1
					elif json1_data['09:00 AM to 09:59 AM']["status"] == "inactive":
						sheet11.write(row,col+x+10,json1_data['09:00 AM to 09:59 AM']['steps'],format_red_con)

					else:
						sheet11.write(row,col+x+10,json1_data['09:00 AM to 09:59 AM']['steps'],format_purple)
					#10
					if json1_data['10:00 AM to 10:59 AM']["status"] == "sleeping":
						sheet11.write(row,col+x+11,json1_data['10:00 AM to 10:59 AM']['steps'],format_orange)
						if json1_data['10:00 AM to 10:59 AM']['steps'] >= 300:
							days_count['10:00 AM to 10:59 AM']+= 1
					elif json1_data['10:00 AM to 10:59 AM']["status"] == "active":
						sheet11.write(row,col+x+11,json1_data['10:00 AM to 10:59 AM']['steps'],format_green)
						if json1_data['10:00 AM to 10:59 AM']['steps'] >= 300:
							days_count['10:00 AM to 10:59 AM']+= 1
					elif json1_data['10:00 AM to 10:59 AM']["status"] == "inactive":
						sheet11.write(row,col+x+11,json1_data['10:00 AM to 10:59 AM']['steps'],format_red_con)
					else:
						sheet11.write(row,col+x+11,json1_data['10:00 AM to 10:59 AM']['steps'],format_purple)
					#11
					if json1_data['11:00 AM to 11:59 AM']["status"] == "sleeping":
						sheet11.write(row,col+x+12,json1_data['11:00 AM to 11:59 AM']['steps'],format_orange)
						if json1_data['11:00 AM to 11:59 AM']['steps'] >= 300:
							days_count['11:00 AM to 11:59 AM']+= 1
					elif json1_data['11:00 AM to 11:59 AM']["status"] == "active":
						sheet11.write(row,col+x+12,json1_data['11:00 AM to 11:59 AM']['steps'],format_green)
						if json1_data['11:00 AM to 11:59 AM']['steps'] >= 300:
							days_count['11:00 AM to 11:59 AM']+= 1
					elif json1_data['11:00 AM to 11:59 AM']["status"] == "inactive":
						sheet11.write(row,col+x+12,json1_data['11:00 AM to 11:59 AM']['steps'],format_red_con)
					else:
						sheet11.write(row,col+x+12,json1_data['11:00 AM to 11:59 AM']['steps'],format_purple)
					#12
					if json1_data['12:00 PM to 12:59 PM']["status"] == "sleeping":
						sheet11.write(row,col+x+13,json1_data['12:00 PM to 12:59 PM']['steps'],format_orange)
						if json1_data['12:00 PM to 12:59 PM']['steps'] >= 300:
							days_count['12:00 PM to 12:59 PM'] += 1
					elif json1_data['12:00 PM to 12:59 PM']["status"] == "active":
						sheet11.write(row,col+x+13,json1_data['12:00 PM to 12:59 PM']['steps'],format_green)
						if json1_data['12:00 PM to 12:59 PM']['steps'] >= 300:
							days_count['12:00 PM to 12:59 PM'] += 1
					elif json1_data['12:00 PM to 12:59 PM']["status"] == "inactive":
						sheet11.write(row,col+x+13,json1_data['12:00 PM to 12:59 PM']['steps'],format_red_con)
					else:
						sheet11.write(row,col+x+13,json1_data['12:00 PM to 12:59 PM']['steps'],format_purple)
					#1
					if json1_data['01:00 PM to 01:59 PM']["status"] == "sleeping":
						sheet11.write(row,col+x+14,json1_data['01:00 PM to 01:59 PM']['steps'],format_orange)
						if json1_data['01:00 PM to 01:59 PM']['steps'] >= 300:
							days_count['01:00 PM to 01:59 PM']+= 1
					elif json1_data['01:00 PM to 01:59 PM']["status"] == "active":
						sheet11.write(row,col+x+14,json1_data['01:00 PM to 01:59 PM']['steps'],format_green)
						if json1_data['01:00 PM to 01:59 PM']['steps'] >= 300:
							days_count['01:00 PM to 01:59 PM']+= 1
					elif json1_data['01:00 PM to 01:59 PM']["status"] == "inactive":
						sheet11.write(row,col+x+14,json1_data['01:00 PM to 01:59 PM']['steps'],format_red_con)
					else:
						sheet11.write(row,col+x+14,json1_data['01:00 PM to 01:59 PM']['steps'],format_purple)
					#2
					if json1_data['02:00 PM to 02:59 PM']["status"] == "sleeping":
						sheet11.write(row,col+x+15,json1_data['02:00 PM to 02:59 PM']['steps'],format_orange)
						if json1_data['02:00 PM to 02:59 PM']['steps'] >= 300:
							days_count['02:00 PM to 02:59 PM']+= 1
					elif json1_data['02:00 PM to 02:59 PM']["status"] == "active":
						sheet11.write(row,col+x+15,json1_data['02:00 PM to 02:59 PM']['steps'],format_green)
						if json1_data['02:00 PM to 02:59 PM']['steps'] >= 300:
							days_count['02:00 PM to 02:59 PM']+= 1
					elif json1_data['02:00 PM to 02:59 PM']["status"] == "inactive":
						sheet11.write(row,col+x+15,json1_data['02:00 PM to 02:59 PM']['steps'],format_red_con)
					else:
						sheet11.write(row,col+x+15,json1_data['02:00 PM to 02:59 PM']['steps'],format_purple)
					#3
					if json1_data['03:00 PM to 03:59 PM']["status"] == "sleeping":
						sheet11.write(row,col+x+16,json1_data['03:00 PM to 03:59 PM']['steps'],format_orange)
						if json1_data['03:00 PM to 03:59 PM']['steps'] >= 300:
							days_count['03:00 PM to 03:59 PM']+= 1
					elif json1_data['03:00 PM to 03:59 PM']["status"] == "active":
						sheet11.write(row,col+x+16,json1_data['03:00 PM to 03:59 PM']['steps'],format_green)
						if json1_data['03:00 PM to 03:59 PM']['steps'] >= 300:
							days_count['03:00 PM to 03:59 PM']+= 1
					elif json1_data['03:00 PM to 03:59 PM']["status"] == "inactive":
						sheet11.write(row,col+x+16,json1_data['03:00 PM to 03:59 PM']['steps'],format_red_con)
					else:
						sheet11.write(row,col+x+16,json1_data['03:00 PM to 03:59 PM']['steps'],format_purple)
					#4
					if json1_data['04:00 PM to 04:59 PM']["status"] == "sleeping":
						sheet11.write(row,col+x+17,json1_data['04:00 PM to 04:59 PM']['steps'],format_orange)
						if json1_data['04:00 PM to 04:59 PM']['steps'] >= 300:
							days_count['04:00 PM to 04:59 PM']+= 1
					elif json1_data['04:00 PM to 04:59 PM']["status"] == "active":
						sheet11.write(row,col+x+17,json1_data['04:00 PM to 04:59 PM']['steps'],format_green)
						if json1_data['04:00 PM to 04:59 PM']['steps'] >= 300:
							days_count['04:00 PM to 04:59 PM']+= 1
					elif json1_data['04:00 PM to 04:59 PM']["status"] == "inactive":
						sheet11.write(row,col+x+17,json1_data['04:00 PM to 04:59 PM']['steps'],format_red_con)
					else:
						sheet11.write(row,col+x+17,json1_data['04:00 PM to 04:59 PM']['steps'],format_purple)
					#5
					if json1_data['05:00 PM to 05:59 PM']["status"] == "sleeping":
						sheet11.write(row,col+x+18,json1_data['05:00 PM to 05:59 PM']['steps'],format_orange)
						if json1_data['05:00 PM to 05:59 PM']['steps'] >= 300:
							days_count['05:00 PM to 05:59 PM']+= 1
					elif json1_data['05:00 PM to 05:59 PM']["status"] == "active":
						sheet11.write(row,col+x+18,json1_data['05:00 PM to 05:59 PM']['steps'],format_green)
						if json1_data['05:00 PM to 05:59 PM']['steps'] >= 300:
							days_count['05:00 PM to 05:59 PM']+= 1
					elif json1_data['05:00 PM to 05:59 PM']["status"] == "inactive":
						sheet11.write(row,col+x+18,json1_data['05:00 PM to 05:59 PM']['steps'],format_red_con)
					else:
						sheet11.write(row,col+x+18,json1_data['05:00 PM to 05:59 PM']['steps'],format_purple)
					#6
					if json1_data['06:00 PM to 06:59 PM']["status"] == "sleeping":
						sheet11.write(row,col+x+19,json1_data['06:00 PM to 06:59 PM']['steps'],format_orange)
						if json1_data['06:00 PM to 06:59 PM']['steps'] >= 300:
							days_count['06:00 PM to 06:59 PM']+= 1
					elif json1_data['06:00 PM to 06:59 PM']["status"] == "active":
						sheet11.write(row,col+x+19,json1_data['06:00 PM to 06:59 PM']['steps'],format_green)
						if json1_data['06:00 PM to 06:59 PM']['steps'] >= 300:
							days_count['06:00 PM to 06:59 PM']+= 1
					elif json1_data['06:00 PM to 06:59 PM']["status"] == "inactive":
						sheet11.write(row,col+x+19,json1_data['06:00 PM to 06:59 PM']['steps'],format_red_con)
					else:
						sheet11.write(row,col+x+19,json1_data['06:00 PM to 06:59 PM']['steps'],format_purple)
					#7
					if json1_data['07:00 PM to 07:59 PM']["status"] == "sleeping":
						sheet11.write(row,col+x+20,json1_data['07:00 PM to 07:59 PM']['steps'],format_orange)
						if json1_data['07:00 PM to 07:59 PM']['steps'] >= 300:
							days_count['07:00 PM to 07:59 PM']+= 1
					elif json1_data['07:00 PM to 07:59 PM']["status"] == "active":
						sheet11.write(row,col+x+20,json1_data['07:00 PM to 07:59 PM']['steps'],format_green)
						if json1_data['07:00 PM to 07:59 PM']['steps'] >= 300:
							days_count['07:00 PM to 07:59 PM']+= 1
					elif json1_data['07:00 PM to 07:59 PM']["status"] == "inactive":
						sheet11.write(row,col+x+20,json1_data['07:00 PM to 07:59 PM']['steps'],format_red_con)
					else:
						sheet11.write(row,col+x+20,json1_data['07:00 PM to 07:59 PM']['steps'],format_purple)
					#8
					if json1_data['08:00 PM to 08:59 PM']["status"] == "sleeping":
						sheet11.write(row,col+x+21,json1_data['08:00 PM to 08:59 PM']['steps'],format_orange)
						if json1_data['08:00 PM to 08:59 PM']['steps'] >= 300:
							days_count['08:00 PM to 08:59 PM']+= 1
					elif json1_data['08:00 PM to 08:59 PM']["status"] == "active":
						sheet11.write(row,col+x+21,json1_data['08:00 PM to 08:59 PM']['steps'],format_green)
						if json1_data['08:00 PM to 08:59 PM']['steps'] >= 300:
							days_count['08:00 PM to 08:59 PM']+= 1
					elif json1_data['08:00 PM to 08:59 PM']["status"] == "inactive":
						sheet11.write(row,col+x+21,json1_data['08:00 PM to 08:59 PM']['steps'],format_red_con)
					else:
						sheet11.write(row,col+x+21,json1_data['08:00 PM to 08:59 PM']['steps'],format_purple)
					#9
					if json1_data['09:00 PM to 09:59 PM']["status"] == "sleeping":
						sheet11.write(row,col+x+22,json1_data['09:00 PM to 09:59 PM']['steps'],format_orange)
						if json1_data['09:00 PM to 09:59 PM']['steps'] >= 300:
							days_count['09:00 PM to 09:59 PM']+= 1
					elif json1_data['09:00 PM to 09:59 PM']["status"] == "active":
						sheet11.write(row,col+x+22,json1_data['09:00 PM to 09:59 PM']['steps'],format_green)
						if json1_data['09:00 PM to 09:59 PM']['steps'] >= 300:
							days_count['09:00 PM to 09:59 PM']+= 1
					elif json1_data['09:00 PM to 09:59 PM']["status"] == "inactive":
						sheet11.write(row,col+x+22,json1_data['09:00 PM to 09:59 PM']['steps'],format_red_con)
					else:
						sheet11.write(row,col+x+22,json1_data['09:00 PM to 09:59 PM']['steps'],format_purple)
					#10
					if json1_data['10:00 PM to 10:59 PM']["status"] == "sleeping":
						sheet11.write(row,col+x+23,json1_data['10:00 PM to 10:59 PM']['steps'],format_orange)
						if json1_data['10:00 PM to 10:59 PM']['steps'] >= 300:
							days_count['10:00 PM to 10:59 PM']+= 1
					elif json1_data['10:00 PM to 10:59 PM']["status"] == "active":
						sheet11.write(row,col+x+23,json1_data['10:00 PM to 10:59 PM']['steps'],format_green)
						if json1_data['10:00 PM to 10:59 PM']['steps'] >= 300:
							days_count['10:00 PM to 10:59 PM']+= 1
					elif json1_data['10:00 PM to 10:59 PM']["status"] == "inactive":
						sheet11.write(row,col+x+23,json1_data['10:00 PM to 10:59 PM']['steps'],format_red_con)
					else:
						sheet11.write(row,col+x+23,json1_data['10:00 PM to 10:59 PM']['steps'],format_purple)
					#11
					if json1_data['11:00 PM to 11:59 PM']["status"] == "sleeping":
						sheet11.write(row,col+x+24,json1_data['11:00 PM to 11:59 PM']['steps'],format_orange)
						if json1_data['11:00 PM to 11:59 PM']['steps'] >= 300:
							days_count['11:00 PM to 11:59 PM']+= 1
					elif json1_data['11:00 PM to 11:59 PM']["status"] == "active":
						sheet11.write(row,col+x+24,json1_data['11:00 PM to 11:59 PM']['steps'],format_green)
						if json1_data['11:00 PM to 11:59 PM']['steps'] >= 300:
							days_count['11:00 PM to 11:59 PM']+= 1
					elif json1_data['11:00 PM to 11:59 PM']["status"] == "inactive":
						sheet11.write(row,col+x+24,json1_data['11:00 PM to 11:59 PM']['steps'],format_red_con)
					else:
						sheet11.write(row,col+x+24,json1_data['11:00 PM to 11:59 PM']['steps'],format_purple)
					# sheet11.write(row,col+x+2,json1_data['01:00 AM to 01:59 AM']['steps'])
					# sheet11.write(row,col+x+3,json1_data['02:00 AM to 02:59 AM']['steps'])
					# sheet11.write(row,col+x+4,json1_data['03:00 AM to 03:59 AM']['steps'])
					# sheet11.write(row,col+x+5,json1_data['04:00 AM to 04:59 AM']['steps'])
					# sheet11.write(row,col+x+6,json1_data['05:00 AM to 05:59 AM']['steps'])
					# sheet11.write(row,col+x+7,json1_data['06:00 AM to 06:59 AM']['steps'])
					# sheet11.write(row,col+x+8,json1_data['07:00 AM to 07:59 AM']['steps'])
					# sheet11.write(row,col+x+9,json1_data['08:00 AM to 08:59 AM']['steps'])
					# sheet11.write(row,col+x+10,json1_data['09:00 AM to 09:59 AM']['steps'])
					# sheet11.write(row,col+x+11,json1_data['10:00 AM to 10:59 AM']['steps'])
					# sheet11.write(row,col+x+12,json1_data['11:00 AM to 11:59 AM']['steps'])
					# sheet11.write(row,col+x+13,json1_data['12:00 PM to 12:59 PM']['steps'])
					# sheet11.write(row,col+x+14,json1_data['01:00 PM to 01:59 PM']['steps'])
					# sheet11.write(row,col+x+15,json1_data['02:00 PM to 02:59 PM']['steps'])
					# sheet11.write(row,col+x+16,json1_data['03:00 PM to 03:59 PM']['steps'])
					# sheet11.write(row,col+x+17,json1_data['04:00 PM to 04:59 PM']['steps'])
					# sheet11.write(row,col+x+18,json1_data['05:00 PM to 05:59 PM']['steps'])
					# sheet11.write(row,col+x+19,json1_data['06:00 PM to 06:59 PM']['steps'])
					# sheet11.write(row,col+x+20,json1_data['07:00 PM to 07:59 PM']['steps'])
					# sheet11.write(row,col+x+21,json1_data['08:00 PM to 08:59 PM']['steps'])
					# sheet11.write(row,col+x+22,json1_data['09:00 PM to 09:59 PM']['steps'])
					# sheet11.write(row,col+x+23,json1_data['10:00 PM to 10:59 PM']['steps'])
					# sheet11.write(row,col+x+24,json1_data['11:00 PM to 11:59 PM']['steps'])
					def format_active_prcnt(days_count,time_slot,total_days):
						if total_days:
							prcnt = round((days_count.get(time_slot,0) / total_days) * 100,2)
							return str(prcnt) + " %"
						return str(0)+" %"

					sheet11.write(row,col+x+25,json1_data['sleeping_hours'])
					sheet11.write(row,col+x+26,json1_data['active_hours'])
					sheet11.write(row,col+x+27,json1_data['inactive_hours'])
					sheet11.write(row,col+x+28,json1_data.get('strength_hours',0))
					sheet11.write(5,2+1,str(round(((days_count["12:00 AM to 12:59 AM"]/total_days))*100,2))+" %",bold)
					# print(((days_count["12:00 AM to 12:59 AM"]/total_days))*100)
					sheet11.write(5,2+2,format_active_prcnt(days_count,'01:00 AM to 01:59 AM',total_days),bold)
					sheet11.write(5,2+3,str(round(((days_count["02:00 AM to 02:59 AM"]/total_days))*100,2))+" %",bold)
					sheet11.write(5,2+4,str(round(((days_count["03:00 AM to 03:59 AM"]/total_days))*100,2))+" %",bold)
					sheet11.write(5,2+5,str(round(((days_count["04:00 AM to 04:59 AM"]/total_days))*100,2))+" %",bold)
					sheet11.write(5,2+6,str(round(((days_count["05:00 AM to 05:59 AM"]/total_days))*100,2))+" %",bold)
					sheet11.write(5,2+7,str(round(((days_count["06:00 AM to 06:59 AM"]/total_days))*100,2))+" %",bold)
					sheet11.write(5,2+8,str(round(((days_count["07:00 AM to 07:59 AM"]/total_days))*100,2))+" %",bold)
					sheet11.write(5,2+9,str(round(((days_count["08:00 AM to 08:59 AM"]/total_days))*100,2))+" %",bold)
					sheet11.write(5,2+10,str(round(((days_count["09:00 AM to 09:59 AM"]/total_days))*100,2))+" %",bold)
					sheet11.write(5,2+11,str(round(((days_count["10:00 AM to 10:59 AM"]/total_days))*100,2))+" %",bold)
					sheet11.write(5,2+12,str(round(((days_count["11:00 AM to 11:59 AM"]/total_days))*100,2))+" %",bold)
					sheet11.write(5,2+13,str(round(((days_count["12:00 PM to 12:59 PM"]/total_days))*100,2))+" %",bold)
					sheet11.write(5,2+14,str(round(((days_count["01:00 PM to 01:59 PM"]/total_days))*100,2))+" %",bold)
					sheet11.write(5,2+15,str(round(((days_count["02:00 PM to 02:59 PM"]/total_days))*100,2))+" %",bold)
					sheet11.write(5,2+16,str(round(((days_count["03:00 PM to 03:59 PM"]/total_days))*100,2))+" %",bold)
					sheet11.write(5,2+17,str(round(((days_count["04:00 PM to 04:59 PM"]/total_days))*100,2))+" %",bold)
					sheet11.write(5,2+18,str(round(((days_count["05:00 PM to 05:59 PM"]/total_days))*100,2))+" %",bold)
					sheet11.write(5,2+19,str(round(((days_count["06:00 PM to 06:59 PM"]/total_days))*100,2))+" %",bold)
					sheet11.write(5,2+20,str(round(((days_count["07:00 PM to 07:59 PM"]/total_days))*100,2))+" %",bold)
					sheet11.write(5,2+21,str(round(((days_count["08:00 PM to 08:59 PM"]/total_days))*100,2))+" %",bold)
					sheet11.write(5,2+22,str(round(((days_count["09:00 PM to 09:59 PM"]/total_days))*100,2))+" %",bold)
					sheet11.write(5,2+23,str(round(((days_count["10:00 PM to 10:59 PM"]/total_days))*100,2))+" %",bold)
					sheet11.write(5,2+24,str(round(((days_count["11:00 PM to 11:59 PM"]/total_days))*100,2))+" %",bold)




			# for x,key in enumerate(columns):
			# 	steps_string = steps_data['movement_consistency']
			# 	if steps_string:
			# 		json1_data = json.loads(steps_string)
			# 		sheet11.write_row(row,col+x,json1_data['total_steps'])
					# if json1_data['12:00 AM to 12:59 AM']["status"] == "sleeping":
					# 	sheet11.write(row,col+x+1,json1_data['12:00 AM to 12:59 AM']['steps'],format_orange)
					# elif json1_data['12:00 AM to 12:59 AM']["status"] == "active":
					# 	sheet11.write(row,col+x+1,json1_data['12:00 AM to 12:59 AM']['steps'],format_green)
					# elif json1_data['12:00 AM to 12:59 AM']["status"] == "inactive":
					# 	sheet11.write(row,col+x+1,json1_data['12:00 AM to 12:59 AM']['steps'],format_red)
					# else:
					# 	sheet11.write(row,col+x+1,json1_data['12:00 AM to 12:59 AM']['steps'],format_purple)
						
						# sheet11.write(row,col+x+2,json1_data['01:00 AM to 01:59 AM']['steps'])
						# sheet11.write(row,col+x+3,json1_data['02:00 AM to 02:59 AM']['steps'])
						# sheet11.write(row,col+x+4,json1_data['03:00 AM to 03:59 AM']['steps'])
						# sheet11.write(row,col+x+5,json1_data['04:00 AM to 04:59 AM']['steps'])
						# sheet11.write(row,col+x+6,json1_data['05:00 AM to 05:59 AM']['steps'])
						# sheet11.write(row,col+x+7,json1_data['06:00 AM to 06:59 AM']['steps'])
						# sheet11.write(row,col+x+8,json1_data['07:00 AM to 07:59 AM']['steps'])
						# sheet11.write(row,col+x+9,json1_data['08:00 AM to 08:59 AM']['steps'])
						# sheet11.write(row,col+x+10,json1_data['09:00 AM to 09:59 AM']['steps'])
						# sheet11.write(row,col+x+11,json1_data['10:00 AM to 10:59 AM']['steps'])
						# sheet11.write(row,col+x+12,json1_data['11:00 AM to 11:59 AM']['steps'])
						# sheet11.write(row,col+x+13,json1_data['12:00 PM to 12:59 PM']['steps'])
						# sheet11.write(row,col+x+14,json1_data['01:00 PM to 01:59 PM']['steps'])
						# sheet11.write(row,col+x+15,json1_data['02:00 PM to 02:59 PM']['steps'])
						# sheet11.write(row,col+x+16,json1_data['03:00 PM to 03:59 PM']['steps'])
						# sheet11.write(row,col+x+17,json1_data['04:00 PM to 04:59 PM']['steps'])
						# sheet11.write(row,col+x+18,json1_data['05:00 PM to 05:59 PM']['steps'])
						# sheet11.write(row,col+x+19,json1_data['06:00 PM to 06:59 PM']['steps'])
						# sheet11.write(row,col+x+20,json1_data['07:00 PM to 07:59 PM']['steps'])
						# sheet11.write(row,col+x+21,json1_data['08:00 PM to 08:59 PM']['steps'])
						# sheet11.write(row,col+x+22,json1_data['09:00 PM to 09:59 PM']['steps'])
						# sheet11.write(row,col+x+23,json1_data['10:00 PM to 10:59 PM']['steps'])
						# sheet11.write(row,col+x+24,json1_data['11:00 PM to 11:59 PM']['steps'])
						# sheet11.write(row,col+x+25,json1_data['sleeping_hours'])
						# sheet11.write(row,col+x+26,json1_data['active_hours'])
						# sheet11.write(row,col+x+27,json1_data['inactive_hours'])
						# sheet11.write(row,col+x+28,json1_data.get('strength_hours',0))


		else:
			row += 1
			sheet11.write(row,col,'')
		current_date -= timedelta(days=1)

	#Progress Analyzer

	# json_cum = open('/home/normsoftware/WORK/JVB/pa_dummy.json')
	# json_cum_str = json_cum.read()
	# json_cum1 = json.loads(json_cum_str)
	# print(json_cum1['summary']['nutrition']['prcnt_unprocessed_food_gpa']['custom_range']['2018-02-12 to 2018-02-18'])

	book.close()
	return response

# def export_movement_consistency_xls(request):
# 	to_date = request.GET.get('to_date',None)
# 	from_date = request.GET.get('from_date', None)

# 	to_date = datetime.strptime(to_date, "%m-%d-%Y").date()
# 	from_date = datetime.strptime(from_date, "%m-%d-%Y").date()
# 	filename = '{}_Movemenr_Consistency_data.xlsx'.format(request.user.username)
# 	response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
# 	response['Content-Disposition'] = "attachment; filename={}".format(filename)
# 	book = Workbook(response,{'in_memory': True})
# 	sheet11 = book.add_worksheet('Movement Consistency')
# 	date_format = book.add_format({'num_format': 'm-d-yy'})
# 	# steps_qs = Steps.objects.filter(
# 	# 	user_ql__created_at__range=(from_date, to_date),
# 	# 	user_ql__user = request.user).order_by('-user_ql__created_at')

# 	# steps_datewise = {q.user_ql.created_at.strftime("%Y-%m-%d"):q
# 	# 	 for q in steps_qs }
# 	current_date = to_date
# 	r = 4
# 	# ?from_date=01-31-2018&to_date=01-05-2018
# 	if to_date and from_date:
# 		while (current_date >= from_date):
# 			r = r + 1
# 			sheet11.write(r,0,current_date,date_format)
# 			current_date -= timedelta(days = 1)
# 	sheet11.set_row(3,45)
# 	steps_qs = Steps.objects.filter(
# 		user_ql__created_at__range=(from_date, to_date),
# 		user_ql__user = request.user).order_by('-user_ql__created_at')

# 	steps_datewise = {q.user_ql.created_at.strftime("%Y-%m-%d"):q
# 		 for q in steps_qs }
# 	sheet11.write(2,0,"Hour")
# 	sheet11.write(3,0,"Date")
# 	sheet11.write(3,1,"Daily Movement Consistency Score")
# 	hours_range = ["Total Daily Steps","12:00 AM to 12:59 AM","01:00 AM to 01:59 AM","02:00 AM to 02:59 AM","03:00 AM to 03:59 AM","04:00 AM to 04:59 AM",
# 	"05:00 AM to 05:59 AM","06:00 AM to 06:59 AM","07:00 AM to 07:59 AM","08:00 AM to 08:59 AM","09:00 AM to 09:59 AM","10:00 AM to 10:59 AM","11:00 AM to 11:59 AM",
# 	"12:00 PM to 12:59 PM","01:00 PM to 01:59 PM","02:00 PM to 02:59 PM","03:00 PM to 03:59 PM","04:00 PM to 04:59 PM","05:00 PM to 05:59 PM",
# 	"06:00 PM to 06:59 PM","07:00 PM to 07:59 PM","08:00 PM to 08:59 PM","09:00 PM to 09:59 PM","10:00 PM to 10:59 PM","11:00 PM to 11:59 PM","Sleeping Hours",
# 	"Active Hours","Inactive Hours","Strength Hours"]
# 	hours_range1 = ["total_steps","12:00 AM to 12:59 AM","01:00 AM to 01:59 AM","02:00 AM to 02:59 AM","03:00 AM to 03:59 AM","04:00 AM to 04:59 AM",
# 	"05:00 AM to 05:59 AM","06:00 AM to 06:59 AM","07:00 AM to 07:59 AM","08:00 AM to 08:59 AM","09:00 AM to 09:59 AM","10:00 AM to 10:59 AM","11:00 AM to 11:59 AM",
# 	"12:00 PM to 12:59 PM","01:00 PM to 01:59 PM","02:00 PM to 02:59 PM","03:00 PM to 03:59 PM","04:00 PM to 04:59 PM","05:00 PM to 05:59 PM",
# 	"06:00 PM to 06:59 PM","07:00 PM to 07:59 PM","08:00 PM to 08:59 PM","09:00 PM to 09:59 PM","10:00 PM to 10:59 PM","11:00 PM to 11:59 PM","sleeping_hours",
# 	"active_hours","inactive_hours"]
# 	columns = ['movement_consistency']
# 	col_num = 2
# 	start_num = 12
# 	start_digit =':01'
# 	end_digit = ':59'
# 	for hour in range(1,25,1):
# 		col_num += 1
# 		sheet11.write(2,col_num,hour)
# 	col_num1 = 1
# 	for col_num in range(len(hours_range)):
# 		col_num1 += 1
# 		sheet11.write(3,col_num1,hours_range[col_num])
# 	current_date = to_date
# 	row_num = 4
# 	row = 4
# 	col = 2
# 	while (current_date >= from_date):
# 		steps_data = steps_datewise.get(current_date.strftime("%Y-%m-%d"),None)
# 		if steps_data:
# 			steps_data = steps_data.__dict__
# 			# logic
# 			row += 1
# 			# print(steps_data)
# 			for x,key in enumerate(columns):
# 				steps_string = steps_data['movement_consistency']
# 				if steps_string:
# 					json1_data = json.loads(steps_string)
# 					# print (json1_data)
# 					# print(json1_data.keys())
# 					# if json1_data['12:00 AM to 12:59 AM']
# 					# row += 1
# 					sheet11.write(row,col+x,json1_data['total_steps'])
# 					sheet11.write(row,col+x+1,json1_data['12:00 AM to 12:59 AM']['steps'])
# 					sheet11.write(row,col+x+2,json1_data['01:00 AM to 01:59 AM']['steps'])
# 					sheet11.write(row,col+x+3,json1_data['02:00 AM to 02:59 AM']['steps'])
# 					sheet11.write(row,col+x+4,json1_data['03:00 AM to 03:59 AM']['steps'])
# 					sheet11.write(row,col+x+5,json1_data['04:00 AM to 04:59 AM']['steps'])
# 					sheet11.write(row,col+x+6,json1_data['05:00 AM to 05:59 AM']['steps'])
# 					sheet11.write(row,col+x+7,json1_data['06:00 AM to 06:59 AM']['steps'])
# 					sheet11.write(row,col+x+8,json1_data['07:00 AM to 07:59 AM']['steps'])
# 					sheet11.write(row,col+x+9,json1_data['08:00 AM to 08:59 AM']['steps'])
# 					sheet11.write(row,col+x+10,json1_data['09:00 AM to 09:59 AM']['steps'])
# 					sheet11.write(row,col+x+11,json1_data['10:00 AM to 10:59 AM']['steps'])
# 					sheet11.write(row,col+x+12,json1_data['11:00 AM to 11:59 AM']['steps'])
# 					sheet11.write(row,col+x+13,json1_data['12:00 PM to 12:59 PM']['steps'])
# 					sheet11.write(row,col+x+14,json1_data['01:00 PM to 01:59 PM']['steps'])
# 					sheet11.write(row,col+x+15,json1_data['02:00 PM to 02:59 PM']['steps'])
# 					sheet11.write(row,col+x+16,json1_data['03:00 PM to 03:59 PM']['steps'])
# 					sheet11.write(row,col+x+17,json1_data['04:00 PM to 04:59 PM']['steps'])
# 					sheet11.write(row,col+x+18,json1_data['05:00 PM to 05:59 PM']['steps'])
# 					sheet11.write(row,col+x+19,json1_data['06:00 PM to 06:59 PM']['steps'])
# 					sheet11.write(row,col+x+20,json1_data['07:00 PM to 07:59 PM']['steps'])
# 					sheet11.write(row,col+x+21,json1_data['08:00 PM to 08:59 PM']['steps'])
# 					sheet11.write(row,col+x+22,json1_data['09:00 PM to 09:59 PM']['steps'])
# 					sheet11.write(row,col+x+23,json1_data['10:00 PM to 10:59 PM']['steps'])
# 					sheet11.write(row,col+x+24,json1_data['11:00 PM to 11:59 PM']['steps'])
# 					sheet11.write(row,col+x+25,json1_data['sleeping_hours'])
# 					sheet11.write(row,col+x+26,json1_data['active_hours'])
# 					sheet11.write(row,col+x+27,json1_data['inactive_hours'])
# 					sheet11.write(row,col+x+28,json1_data.get['strength_hours',0])


# 			# for x,key1 in enumerate(hours_range1):
# 			# 	if json1_data[key1]['status'] == 'active':
# 			# 		sheet11.write.(row,column,json1_data[key1]['steps'])
# 			# 	else:
# 			# 		sheet11.write.(row,column,json1_data[key1]['steps'])


# 		else:
# 			row += 1
# 			sheet11.write(row,col,'')
# 		current_date -= timedelta(days=1)

	
# 	book.close()
# 	return response