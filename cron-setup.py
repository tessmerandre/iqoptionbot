import json
from crontab import CronTab
from datetime import datetime
import os

month_day = datetime.now().strftime('%d %m')

def get_times():
    with open('/bot/bets.json') as json_file:
        return json.load(json_file)

def create_crons():
    with CronTab(user='root') as cron:
        cron.remove_all()
        for time in get_times():
            job = cron.new(command='python3 /bot/bet-manager.py {} fraterdu'.format(time))
            cron_str = get_cron_time_str(time)
            job.setall(cron_str)

def get_cron_time_str(time):
    print(time)
    splitted = time.split(':')
    minute = int(splitted[1]) -1 if splitted[1] != '00' else 59
    hour = int(splitted[0]) if minute != 59 else int(splitted[0]) - 1
    
    return '{} {} {} *'.format(minute, hour, month_day)


create_crons()

