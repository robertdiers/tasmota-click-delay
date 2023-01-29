#!/usr/bin/env python

import configparser
import os
from datetime import datetime
from paho.mqtt import client as mqtt_client
import time
import json

#read config
config = configparser.ConfigParser()
tasmota_name = 'unknown'

searchattributes = []
valueattributes = {}

def on(client):
    global tasmota_name   
    topic = "cmnd/" + tasmota_name + "/Power"
    #print(topic + " on")
    client.publish(topic, "ON")

def off(client):
    global tasmota_name   
    topic = "cmnd/" + tasmota_name + "/Power"
    #print(topic + " off")
    client.publish(topic, "OFF")

def flatten_json(y):
    out = {}
    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x
    flatten(y)
    return out

def on_message(client, userdata, message):
    global searchattributes
    global valueattributes
    content = str(message.payload.decode("utf-8"))
    #print(content)
    json_object = flatten_json(json.loads(content))
    #print(json_object)
    for attribute in searchattributes:
        if attribute in json_object:
            valueattributes[attribute] = json_object[attribute]
        else:
            valueattributes[attribute] = "n/a"

def get(client, attributes):
    try:
        global tasmota_name   
        topic = "cmnd/" + tasmota_name + "/Status"
        topicstat = "stat/" + tasmota_name + "/STATUS"
        #print(topic)
        global searchattributes
        global valueattributes
        searchattributes = attributes
        valueattributes = {}
        client.on_message=on_message
        client.subscribe(topicstat)
        client.loop_start()
        #send status request to tasmota
        client.publish(topic, 'status')
        counter = 0
        #wait max 10 sec
        while len(valueattributes) == 0 and counter < 100:
            counter = counter + 1
            time.sleep(0.1)
        client.loop_stop()
        client.unsubscribe(topicstat)
        #print(valueattributes)
        return valueattributes
    except Exception as ex:
        print ("ERROR Tasmota: ", ex) 

def connect():
    #print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " START #####")
    try:
        #read config
        config.read('clickdelay.ini')

        #read config and default values
        circulation_mqtt_broker = config['CirculationSection']['circulation_mqtt_broker']
        circulation_mqtt_port = config['CirculationSection']['circulation_mqtt_port']
        circulation_mqtt_user = config['CirculationSection']['circulation_mqtt_user']
        circulation_mqtt_password = config['CirculationSection']['circulation_mqtt_password']
        circulation_mqtt_name = config['CirculationSection']['circulation_mqtt_name']

        # override with environment variables
        if os.getenv('CIRCULATION_MQTT_BROKER','None') != 'None':
            circulation_mqtt_broker = os.getenv('CIRCULATION_MQTT_BROKER')
            print ("using env: CIRCULATION_MQTT_BROKER")
        if os.getenv('CIRCULATION_MQTT_PORT','None') != 'None':
            circulation_mqtt_port = os.getenv('CIRCULATION_MQTT_PORT')
            print ("using env: CIRCULATION_MQTT_PORT")
        if os.getenv('CIRCULATION_MQTT_USER','None') != 'None':
            circulation_mqtt_user = os.getenv('CIRCULATION_MQTT_USER')
            print ("using env: CIRCULATION_MQTT_USER")
        if os.getenv('CIRCULATION_MQTT_PASSWORD','None') != 'None':
            circulation_mqtt_password = os.getenv('CIRCULATION_MQTT_PASSWORD')
            print ("using env: CIRCULATION_MQTT_PASSWORD")
        if os.getenv('CIRCULATION_MQTT_NAME','None') != 'None':
            circulation_mqtt_name = os.getenv('CIRCULATION_MQTT_NAME')
            print ("using env: CIRCULATION_MQTT_NAME")

        #print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " circulation_mqtt_broker: ", circulation_mqtt_broker)
        #print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " circulation_mqtt_port: ", circulation_mqtt_port)
        #print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " circulation_mqtt_user: ", circulation_mqtt_user)
        #print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " circulation_mqtt_password: ", circulation_mqtt_password)
        #print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " circulation_mqtt_name: ", circulation_mqtt_name)
        
        global tasmota_name        
        tasmota_name = circulation_mqtt_name
        client_id = 'python-mqtt-clickdelay-circulation'

        # Set Connecting Client ID
        client = mqtt_client.Client(client_id)
        client.username_pw_set(circulation_mqtt_user, circulation_mqtt_password)
        client.connect(circulation_mqtt_broker, int(circulation_mqtt_port))

        return client
    except Exception as ex:
        print ("ERROR: ", ex)    
        print(ex)
