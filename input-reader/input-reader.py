#!/usr/bin/env python2

import json

M_TYPE = 'm'
INPUT_TYPE = M_TYPE

def read_input():
    file = open('input.txt', 'r')
    text = file.read()
    file.close()
    
    bets = []
    
    lines = text.split('\n')
    for line in lines:
        time = None
        bet = {}
        properties = line.split(' ')
        
        if INPUT_TYPE == M_TYPE:
            bet['candle_time'] = int(properties[0].replace('M', ''))
            bet['currency'] = properties[1]
            bet['action'] = properties[3].lower()
            time = properties[2]
        else:
            bet['candle_time'] = 5
            bet['currency'] = properties[0]
            bet['action'] = properties[2].lower()
            time = properties[1]
        
        print('\"{}\": [{}],'.format(time, bet))
        
        bets.append(bet)

read_input()