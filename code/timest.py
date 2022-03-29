from datetime import datetime
import pytz
def current_time():
	return datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%d/%m/%Y\n%I:%M %p')

def timeStamp():
  return datetime.now(pytz.timezone('Asia/Kolkata'))

import time


def startTIime():
  return int(time.time())

def timeTaken(past_time):
  return (int(time.time())-int(past_time))
