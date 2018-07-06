from datetime import datetime

from django.contrib.auth.models import User

from celery.decorators import task
from celery.utils.log import get_task_logger

from hrr.views import hrr_calculations,\
						store_hhr,\
						store_daily_aa_calculations,\
						store_aa_low_high_end_calculations

logger = get_task_logger(__name__)

@task(name="hrr.save_hrr_data")
def create_hrrdata(user_id,date):
	try:
		user = User.objects.get(id = user_id)
		# start_date = datetime(2018,7,3,0,0,0)
		# date = start_date.strftime("%Y-%m-%d")
		store_hhr(date,user)
		store_daily_aa_calculations(user,date)
		store_aa_low_high_end_calculations(user,date)
	except Exception as e:
		logger.error(e,exc_info=True)