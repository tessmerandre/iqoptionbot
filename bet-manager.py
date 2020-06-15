#!/usr/bin/env python2

import time, json, sys, os, logging
from iqoptionapi.stable_api import IQ_Option
from dateutil import tz
from datetime import datetime
from bet import Bet

def get_logging_filename():
	hour = datetime.now().strftime("%H:%M:%S")
	day_month = datetime.now().strftime("%d-%m")
	return '/logs/{}-{}'.format(day_month, hour)

logging.basicConfig(filename=get_logging_filename(),
					level=logging.INFO,
					format='%(asctime)s %(message)s')

MAX_MARTINGALE = 4

API = IQ_Option('tessmerandre@gmail.com', 'Andre123')
API.connect()
API.change_balance('PRACTICE') # PRACTICE / REAL

while True:
		if API.check_connect() == False:
			print('Error while connecting')
			API.connect()
		else:
			print('Sucessfully connected to the API')
			break
	
		time.sleep(1)

def current_balance():
	return API.get_balance()

def get_amount_for_bet():
	return current_balance() * 0.01

def bet(bets):
	initial_amount = get_amount_for_bet()
	threads = []
	for bet in bets:
		thread = Bet(kwargs= {
			'api': API,
			'bet': bet,
			'initial_amount': initial_amount,
			'max_martingale': MAX_MARTINGALE
		})
		thread.start()
		threads.append(thread)

	for thread in threads:
		thread.join()

	sys.exit()
	

def find_bets():
	time = sys.argv[1]
	with open('/bot/bets.json') as json_file:
		data = json.load(json_file)
		bets = data[time]
		bet(bets)


find_bets()

