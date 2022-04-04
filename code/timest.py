from datetime import datetime
import pytz
def current_time():
	return datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%d/%m/%Y\n%I:%M %p')

