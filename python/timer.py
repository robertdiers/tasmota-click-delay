#!/usr/bin/env python
import TasmotaCirculation

import configparser
import os
import pytz

from datetime import datetime

#read config
config = configparser.ConfigParser()

if __name__ == "__main__":
    try:

        #read config
        config.read('clickdelay.ini')

        #read config and default values
        circulation_hour_on = config['CirculationSection']['circulation_hour_on']
        circulation_hour_off = config['CirculationSection']['circulation_hour_off']
        circulation_time_zone = config['CirculationSection']['circulation_time_zone']
        if os.getenv('CIRCULATION_HOUR_ON','None') != 'None':
            circulation_hour_on = os.getenv('CIRCULATION_HOUR_ON')
        if os.getenv('CIRCULATION_HOUR_OFF','None') != 'None':
            circulation_hour_off = os.getenv('CIRCULATION_HOUR_OFF')
        if os.getenv('CIRCULATION_TIME_ZONE','None') != 'None':
            circulation_time_zone = os.getenv('CIRCULATION_TIME_ZONE')

        #skip execution if lock file exists
        if not os.path.exists(config['CirculationSection']['circulation_lock_filename']):

            #connect to circulation pump
            circulation_client = TasmotaCirculation.connect()

            #read hour
            usedTz = pytz.timezone(circulation_time_zone) 
            currentDateAndTime = datetime.now(usedTz)

            #switch on or off
            if int(currentDateAndTime.hour) >= int(circulation_hour_on) and int(currentDateAndTime.hour) < int(circulation_hour_off):
                print("timer circulation: ON - hour is ", currentDateAndTime.hour)
                TasmotaCirculation.on(circulation_client)
            else:
                print("timer circulation: OFF - hour is ", currentDateAndTime.hour)
                TasmotaCirculation.off(circulation_client)
        
    except Exception as ex1:
        print ("ERROR timer circulation: ", ex1)
