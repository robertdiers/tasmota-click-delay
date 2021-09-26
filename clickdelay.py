#!/usr/bin/env python

from flask import Flask
from threading import Timer
from urllib.request import urlopen
from datetime import datetime
import configparser
from apscheduler.schedulers.background import BackgroundScheduler

#read config
config = configparser.ConfigParser()
config.read('clickdelay.ini')

#init flask
app = Flask(__name__)

#define end points

@app.route('/')
def index():
    f = open("html/index.html", "r")
    return f.read()

@app.route('/zirkulation')
def zirkulation():
    f = open("html/zirkulation.html", "r")
    return f.read()

@app.route('/health')
def health():
    return 'up'

@app.route('/status/<tasmota>')
def status(tasmota):
    propkey = 'tasmota.' + tasmota + '.status'
    statuslink = urlopen(config['TasmotaSection'][propkey])
    return statuslink.read().decode('utf-8')

def internalswitch(tasmota, offonly):
    if 'ON' in status(tasmota) or offonly == 0:
        propkey = 'tasmota.' + tasmota + '.switch'
        switchlink = urlopen(config['TasmotaSection'][propkey])    
        retval = switchlink.read().decode('utf-8')
        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' ' + tasmota + ': ' + retval)
    else:
        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' ' + tasmota + ': already off')

@app.route('/switch/<tasmota>/<waittime>')
def switch(tasmota, waittime):
    internalswitch(tasmota, 0)
    t = Timer(float(waittime), internalswitch, [tasmota, 1])
    t.start() 
    return status(tasmota)

@app.route('/color/<tasmota>')
def color(tasmota):
    if 'ON' in status(tasmota):
        return '#DAF7A6'
    else:
        return '#FF5733'

def checktimer():
    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' ' + ' timer1 check: ' + config['TimerSection']['tasmota.status'])
    currentMonth = datetime.now().month
    currentHour = datetime.now().hour
    activation = config['TimerSection']['timer.'+str(currentMonth)]
    fromTo = activation.split("-")
    #activation during night
    if currentHour >= int(fromTo[0]) or currentHour <= int(fromTo[1]):
        timeractivate()
        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' ' + 'timer1 activated')
    else:
        timerdeactivate()
        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' ' + 'timer1 deactivated')
    return

def timeractivate():
    statuslink = urlopen(config['TimerSection']['tasmota.status'])
    tasmotastatus = statuslink.read().decode('utf-8')
    if 'OFF' in tasmotastatus:
        switchlink = urlopen(config['TimerSection']['tasmota.switch'])    
        retval = switchlink.read().decode('utf-8')
        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' ' + retval)

def timerdeactivate():
    statuslink = urlopen(config['TimerSection']['tasmota.status'])
    tasmotastatus = statuslink.read().decode('utf-8')
    if 'ON' in tasmotastatus:
        switchlink = urlopen(config['TimerSection']['tasmota.switch'])    
        retval = switchlink.read().decode('utf-8')
        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' ' + retval)

sched = BackgroundScheduler(daemon=True)
sched.add_job(checktimer,'interval', minutes=1)
sched.start()
print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' timer1 created every minute')

#start at port 50000
app.run(host='0.0.0.0', port=50000)
