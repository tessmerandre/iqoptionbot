#!/usr/bin/env python2

from iqoptionapi.stable_api import IQ_Option
from threading import Thread
from datetime import datetime
import json, time, logging

class Bet(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, verbose=None):
        super(Bet, self).__init__(group=group, target=target, name=name, verbose=verbose)
        
        self.API = kwargs['api']
        self.bet = kwargs['bet']
        self.amount = kwargs['initial_amount']
        self.max_martingale = kwargs['max_martingale']
    
    def get_payout(self):
        return self.API.get_all_profit()[self.bet['currency']]['turbo']
    
    def update_last_payout(self):
        self.last_payout = self.get_payout()

    def __bet__(self, amount):
        check, bet_id = self.API.buy(amount, self.bet['currency'], self.bet['action'], self.bet['candle_time'])
        if check:
            logging.info('sucessfully bought {} of a {} on {}. bet_id={}'.format(amount, self.bet['action'], self.bet['currency'], bet_id))
        else:
            logging.info('error buying {} of {}. reason={}'.format(amount, self.bet['currency'], bet_id))
        return bet_id
    
    def bet_and_martingale(self, current_martingale=0):
        if current_martingale > self.max_martingale:
            return
        
        new_amount = self.amount
        if (current_martingale != 0 and self.last_profit != 0):
            new_amount = amount + (amount * self.last_payout + 1) / self.last_payout
            logging.info('{}th martingale. currency={}; amount={}; action={}; candle_time={}'.format(current_martingale, self.bet['currency'], new_amount, self.bet['action'], self.bet['candle_time']))
        else:
            while True:
                seconds = datetime.now().strftime('%S')
                if (seconds == '58'):
                    logging.info('1st time buying. currency={}; amount={}; action={}; candle_time={}'.format(self.bet['currency'], new_amount, self.bet['action'], self.bet['candle_time']))
                    break
                
                if (60 - int(seconds) > 30):
                    time.sleep(20)
                else:
                    time.sleep(1)
        
        self.amount = new_amount
        
        bet_id = self.__bet__(new_amount)
        self.update_last_payout()
        
        profit = self.API.check_win_v3(bet_id)
        self.last_profit = profit
        
        if profit <= 0:
            logging.info('LOSS: currency={}; bet_id={}; loss={}; martingale={}'.format(self.bet['currency'], bet_id, profit, current_martingale))
            martingale_time = current_martingale + 1
            self.bet_and_martingale(current_martingale=martingale_time)
        else:
            logging.info('WIN: currency={}; bet_id={}; profit={}'.format(self.bet['currency'], bet_id, profit))
    
    def run(self):
        self.bet_and_martingale()
