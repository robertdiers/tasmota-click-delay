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

def get(client, statusnumber, attributes):
    try:
        global tasmota_name   
        topic = "cmnd/" + tasmota_name + "/Status"
        topicstat = "stat/" + tasmota_name + "/#"
        #print(topic)
        global searchattributes
        global valueattributes
        searchattributes = attributes
        valueattributes = {}
        client.on_message=on_message
        client.subscribe(topicstat)
        client.loop_start()
        #send status request to tasmota
        client.publish(topic, statusnumber)
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
        mqtt_broker = config['MqttSection']['mqtt_broker']
        mqtt_port = config['MqttSection']['mqtt_port']
        mqtt_user = config['MqttSection']['mqtt_user']
        mqtt_password = config['MqttSection']['mqtt_password']
        mqtt_name = config['HeatingSystemSection']['heatingsystemtemp_mqtt_name']

        # override with environment variables
        if os.getenv('MQTT_BROKER','None') != 'None':
            mqtt_broker = os.getenv('MQTT_BROKER')
            #print ("using env: MQTT_BROKER")
        if os.getenv('MQTT_PORT','None') != 'None':
            mqtt_port = os.getenv('MQTT_PORT')
            #print ("using env: MQTT_PORT")
        if os.getenv('MQTT_USER','None') != 'None':
            mqtt_user = os.getenv('MQTT_USER')
            #print ("using env: MQTT_USER")
        if os.getenv('MQTT_PASSWORD','None') != 'None':
            mqtt_password = os.getenv('MQTT_PASSWORD')
            #print ("using env: MQTT_PASSWORD")
        if os.getenv('HEATINGSYSTEMTEMP_MQTT_NAME','None') != 'None':
            mqtt_name = os.getenv('HEATINGSYSTEMTEMP_MQTT_NAME')
            #print ("using env: HEATINGSYSTEMTEMP_MQTT_NAME")

        #print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " heatingsystem mqtt_broker: ", mqtt_broker)
        #print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " heatingsystem mqtt_port: ", mqtt_port)
        #print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " heatingsystem mqtt_user: ", mqtt_user)
        #print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " heatingsystem mqtt_password: ", mqtt_password)
        #print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " heatingsystem mqtt_name: ", mqtt_name)
        
        global tasmota_name        
        tasmota_name = mqtt_name
        client_id = 'python-mqtt-clickdelay-heatingsystemtemp'

        # Set Connecting Client ID
        client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
        client.username_pw_set(mqtt_user, mqtt_password)
        client.connect(mqtt_broker, int(mqtt_port))

        return client
    except Exception as ex:
        print ("ERROR: ", ex)    
        print(ex)
