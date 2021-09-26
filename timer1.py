#!/usr/bin/env python

import configparser
import schedule
from datetime import datetime
from urllib.request import urlopen

#read config
config = configparser.ConfigParser()
config.read('timer1.ini')

def check_timer():
    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' ' + ' timer1 check: ' + config['TimerSection']['tasmota.status'])

    currentMonth = datetime.now().month
    currentHour = datetime.now().hour
    #print(currentMonth)
    #print(currentHour)

    activation = config['TimerSection']['timer.'+str(currentMonth)]
    #print(activation)

    fromTo = activation.split("-")
    #print(fromTo)

    #activation during night
    if currentHour >= int(fromTo[0]) or currentHour <= int(fromTo[1]):
        activate()
        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' ' + 'timer1 activated')
    else:
        deactivate()
        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' ' + 'timer1 deactivated')

    #print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' ' + 'done timer1 execution')
    return

def activate():
    statuslink = urlopen(config['TimerSection']['tasmota.status'])
    tasmotastatus = statuslink.read().decode('utf-8')
    if 'OFF' in tasmotastatus:
        switchlink = urlopen(config['TimerSection']['tasmota.switch'])    
        retval = switchlink.read().decode('utf-8')
        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' ' + retval)

def deactivate():
    statuslink = urlopen(config['TimerSection']['tasmota.status'])
    tasmotastatus = statuslink.read().decode('utf-8')
    if 'ON' in tasmotastatus:
        switchlink = urlopen(config['TimerSection']['tasmota.switch'])    
        retval = switchlink.read().decode('utf-8')
        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' ' + retval)

# execute every hour at minute 1
schedule.every().hour.at(":01").do(check_timer)
print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' timer1 created every hour')

while True:
    schedule.run_pending()
