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
API.change_balance('REAL') # PRACTICE / REAL

while True:
    if API.check_connect() == False:
        logging.info('error while connecting to the API')
        API.connect()
    else:
        logging.info('sucessfully connected to the API')
        break
    
    time.sleep(1)

def current_balance():
	return API.get_balance()

def get_amount_for_bet():
    amount = current_balance() * get_bot_config()['bet-percentage']
    return 2 if amount < 2 else amount

def bet(bets):
	initial_amount = get_amount_for_bet()
	max_martingale = get_bot_config()['max-martingale']
	threads = []
	for bet in bets:
		thread = Bet(kwargs= {
			'api': API,
			'bet': bet,
			'initial_amount': initial_amount,
			'max_martingale': max_martingale
		})
		thread.start()
		threads.append(thread)

	for thread in threads:
		thread.join()

	check_needs_to_stop()

	sys.exit()

def get_bot_config():
    with open('/bot/bot-config.json') as json_file:
        data = json.load(json_file)
        return data[sys.argv[2]]

def check_needs_to_stop():
    config = get_bot_config()
    balance = current_balance()
    if balance <= config['loss-stop'] or balance >= config['win-stop']:
        stop_bot()
    
def stop_bot():
    logging.info('disabling the bot since it reached the win or loss stop')
    current_data = {}
    with open('/bot/bot-config.json') as file:
        current_data = json.load(file)
    
    with open('/bot/bot-config.json', 'w') as outfile:
        config = current_data[sys.argv[2]]
        config['enabled'] = False
        current_data[sys.argv[2]] = config
        json.dump(current_data, outfile)

def find_bets():
	time = sys.argv[1]
	with open('/bot/bets.json') as json_file:
		data = json.load(json_file)
		bets = data[time]
		bet(bets)

config = get_bot_config()
if config['enabled'] == True:
	find_bets()
else:
    logging.info('skipping bet since bot is disabled')
    sys.exit()

