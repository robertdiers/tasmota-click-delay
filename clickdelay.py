#!/usr/bin/env python

from flask import Flask
from threading import Timer
from datetime import datetime
import configparser
import os

import TasmotaCirculation

#read config
config = configparser.ConfigParser()
config.read('clickdelay.ini')


#variables
circulation = 0

#init flask
app = Flask(__name__)

#init Tasmota
TasmotaCirculation.connect()

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
    if 'circulation' in tasmota:
        global circulation
        return circulation
    return 0

def internalon(tasmota):
    if 'circulation' in tasmota:
        TasmotaCirculation.on()
        global circulation
        circulation = 1

def internaloff(tasmota):
    if 'circulation' in tasmota:
        TasmotaCirculation.off()
        global circulation
        circulation = 0

@app.route('/on/<tasmota>/<waittime>')
def on(tasmota, waittime):
    internalon(tasmota)
    t = Timer(float(waittime), internaloff, [tasmota])
    t.start() 
    return 'ON'

@app.route('/color/<tasmota>')
def color(tasmota):
    if status(tasmota) > 0:
        return '#DAF7A6'
    else:
        return '#FF5733'

#start at port 50000
app.run(host='0.0.0.0', port=50000)
