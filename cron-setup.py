import json
from crontab import CronTab
from datetime import datetime
import os

month_day = datetime.now().strftime('%d %m')

def get_bets_filename():
    relative_path = os.path.dirname(os.path.realpath(__file__))
    return 'bets.json' if relative_path == '' else relative_path+'/bets.json'

def get_times():
    with open(get_bets_filename()) as json_file:
        return json.load(json_file)

def create_crons():
    with CronTab(user='root') as cron:
        cron.remove_all()
        for time in get_times():
            job = cron.new(command='python /root/iqoption/bet-manager.py {}'.format(time))
            job.setall(get_cron_time_str(time))

def get_cron_time_str(time):
    splitted = time.split(':')
    minute = int(splitted[1]) -1 if splitted[1] != '00' else 59
    hour = int(splitted[0]) if minute != 59 else int(splitted[0]) - 1
    
    return '{} {} {} *'.format(minute, hour, month_day)


create_crons()

