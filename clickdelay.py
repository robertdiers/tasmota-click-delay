#!/usr/bin/env python

from flask import Flask
from threading import Timer
from urllib.request import urlopen
from datetime import datetime
import configparser
import os

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
    propkey = 'tasmota.' + tasmota + '.ip'
    tasip = config['TasmotaSection'][propkey]
    envkey = 'TASMOTA_'+tasmota.upper()+'_IP'
    print (os.getenv(envkey,'None'))
    if os.getenv(envkey,'None') != 'None':
        tasip = os.getenv(envkey)
        print ("using env: "+envkey)
    statuslink = urlopen('http://'+tasip+'/?m=1')
    return statuslink.read().decode('utf-8')

def internalswitch(tasmota, offonly):
    if 'ON' in status(tasmota) or offonly == 0:
        propkey = 'tasmota.' + tasmota + '.IP'
        tasip = config['TasmotaSection'][propkey]
        envkey = 'TASMOTA_'+tasmota.upper()+'_IP'
        if os.getenv(envkey,'None') != 'None':
            tasip = os.getenv(envkey)
            print ("using env: "+envkey)
        switchlink = urlopen('http://'+tasip+'/?m=1&o=1')
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

#start at port 50000
app.run(host='0.0.0.0', port=50000)
