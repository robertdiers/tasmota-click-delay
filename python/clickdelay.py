#!/usr/bin/env python

from flask import Flask
from threading import Timer
from datetime import datetime
import configparser

import TasmotaCirculation
import TasmotaHeatingSystem
import TasmotaHeatingSystemTemp

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

@app.route('/badheizung')
def badheizung():
    f = open("html/badheizung.html", "r")
    return f.read()

@app.route('/health')
def health():
    return 'up'

@app.route('/status/<tasmota>')
def status(tasmota):
    if 'circulation' in tasmota:
        #as we call only /color/x - cache is not required
        #{"Status":{"Module":1,"DeviceName":"Tasmota_Zirkulation","FriendlyName":["Tasmota_Zirkulation"],"Topic":"tasmota_zirkulation","ButtonTopic":"0","Power":0,"PowerOnState":3,"LedState":1,"LedMask":"FFFF","SaveData":1,"SaveState":1,"SwitchTopic":"0","SwitchMode":[0,0,0,0,0,0,0,0],"ButtonRetain":0,"SwitchRetain":0,"SensorRetain":0,"PowerRetain":0,"InfoRetain":0,"StateRetain":0}}
        circulation_client = TasmotaCirculation.connect()
        result = TasmotaCirculation.get(circulation_client, ["Status_Power"])
        return int(result["Status_Power"])
    if 'badheizung' in tasmota:
        #as we call only /color/x - cache is not required
        #{"Status":{"Module":1,"DeviceName":"Tasmota_Heizungspumpe","FriendlyName":["Tasmota_Heizungspumpe"],"Topic":"tasmota_heizungspumpe","ButtonTopic":"0","Power":0,"PowerOnState":3,"LedState":1,"LedMask":"FFFF","SaveData":1,"SaveState":1,"SwitchTopic":"0","SwitchMode":[0,0,0,0,0,0,0,0],"ButtonRetain":0,"SwitchRetain":0,"SensorRetain":0,"PowerRetain":0,"InfoRetain":0,"StateRetain":0}}
        heatingsystem_client = TasmotaHeatingSystem.connect()
        result = TasmotaHeatingSystem.get(heatingsystem_client, ["Status_Power"])
        return int(result["Status_Power"])
    return 0

@app.route('/value/<tasmota>/<value>')
def value(tasmota, value):
    if 'badheizung' in tasmota:
        heatingsystemtemp_client = TasmotaHeatingSystemTemp.connect()
        result = TasmotaHeatingSystemTemp.get(heatingsystemtemp_client, "8", [value])
        return str(result[value])
    return 'n/a'

def internalon(tasmota):
    if 'circulation' in tasmota:
        #init Tasmota
        circulation_client = TasmotaCirculation.connect()
        TasmotaCirculation.on(circulation_client)
    if 'badheizung' in tasmota:
        #init Tasmota
        heatingsystem_client = TasmotaHeatingSystem.connect()
        TasmotaHeatingSystem.on(heatingsystem_client)
        #turn on light
        heatingsystemtemp_client = TasmotaHeatingSystemTemp.connect()
        TasmotaHeatingSystemTemp.on(heatingsystemtemp_client)

def internaloff(tasmota):
    if 'circulation' in tasmota:
        #init Tasmota
        circulation_client = TasmotaCirculation.connect()
        TasmotaCirculation.off(circulation_client)
    if 'badheizung' in tasmota:
        #init Tasmota
        heatingsystem_client = TasmotaHeatingSystem.connect()
        TasmotaHeatingSystem.off(heatingsystem_client)
        #turn off light
        heatingsystemtemp_client = TasmotaHeatingSystemTemp.connect()
        TasmotaHeatingSystemTemp.off(heatingsystemtemp_client)

@app.route('/on/<tasmota>/<waittime>')
def on(tasmota, waittime):
    internalon(tasmota)
    t = Timer(float(waittime), internaloff, [tasmota])
    t.start() 
    return 'ON'

@app.route('/off/<tasmota>')
def off(tasmota):
    internaloff(tasmota)
    return 'OFF'

@app.route('/color/<tasmota>')
def color(tasmota):
    if status(tasmota) > 0:
        return '#DAF7A6'
    else:
        return '#FF5733'

if __name__ == "__main__":
    #start at port 50000
    app.run(host='0.0.0.0', port=50000)
