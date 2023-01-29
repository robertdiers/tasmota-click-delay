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
    if 'circulation' in tasmota:
        #as we call only /color/x - cache is not required
        #{"Status":{"Module":1,"DeviceName":"Zirkulation","FriendlyName":["Zirkulation"],"Topic":"tasmota_zirkulation","ButtonTopic":"0","Power":0,"PowerOnState":3,"LedState":1,"LedMask":"FFFF","SaveData":1,"SaveState":1,"SwitchTopic":"0","SwitchMode":[0,0,0,0,0,0,0,0],"ButtonRetain":0,"SwitchRetain":0,"SensorRetain":0,"PowerRetain":0,"InfoRetain":0,"StateRetain":0}}
        circulation_client = TasmotaCirculation.connect()
        result = TasmotaCirculation.get(circulation_client, ["Status_Power"])
        return int(result["Status_Power"])
    return 0

def internalon(tasmota):
    if 'circulation' in tasmota:
        #init Tasmota
        circulation_client = TasmotaCirculation.connect()
        TasmotaCirculation.on(circulation_client)

def internaloff(tasmota):
    if 'circulation' in tasmota:
        #init Tasmota
        circulation_client = TasmotaCirculation.connect()
        TasmotaCirculation.off(circulation_client)

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

if __name__ == "__main__":
    #start at port 50000
    app.run(host='0.0.0.0', port=50000)
