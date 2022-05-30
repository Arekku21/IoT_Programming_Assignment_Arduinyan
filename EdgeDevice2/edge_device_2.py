import mysql.connector
import serial
import datetime
import paho.mqtt.client as paho
import os
import json
import paho.mqtt.publish as publish
import time
import sys
import random
import paho.mqtt.client as mqtt
from threading import Thread

ACCESS_TOKEN= 'QafnnZatutodRiykt5lW'               #Token of your device
THINGSBOARD_HOST="thingsboard.cloud"       #host name
port=1883

device = '/dev/ttyACM0' 
arduino = serial.Serial(device, 9600)

button_state = {"Switch_Status":"Toggled"}

def publishValue(client):
    
    while True:
        
        mydb = mysql.connector.connect(host="localhost", user="pi", password="raspberry", database="Db_SmartPetAlarm")
        
        while(arduino.in_waiting == 0):
            pass
        
        line = arduino.readline()
        line = line.decode("utf-8")
        
        pieces = line.split(" ")
        
        switch = pieces[0]
        distance = pieces[1]
        alarm = pieces[2]
        
        myoutput='{"Switch_Status":' + switch + ', "Detection_Distance":' + distance + ', "Alarm_Status":' + alarm + '}'
        
        client.publish("v1/devices/me/telemetry",myoutput) #topic-v1/devices/me/telemetry
        print(myoutput)
        
        with mydb:
            mycursor = mydb.cursor()
            mycursor.execute("INSERT INTO table_alert_logs (Switch_Status, Detection_Distance, Alarm_Status) VALUES (%s,%s,%s)", (switch,distance,alarm))
            mydb.commit()
            mycursor.close()

def setValue(params):
    arduino.write(str("Toggle").encode())
    
def on_connect(client, userdata, flags, rc):
    client.subscribe('v1/devices/me/rpc/request/+')
    
def on_message(client, userdata, msg):
    if msg.topic.startswith('v1/devices/me/rpc/request/'):
        requestId = msg.topic[len('v1/devices/me/rpc/request/'):len(msg.topic)]
        data = json.loads(msg.payload)
        if data['method'] == 'getValue':
            line = arduino.readline()
            line = line.decode("utf-8")
            
            pieces = line.split(" ")
            
            switch = pieces[0]
            distance = pieces[1]
            alarm = pieces[2]
       
            myoutput='{"Switch_Status":' + switch + ', "Detection_Distance":' + distance + ', "Alarm_Status":' + alarm + '}'
            
            client.publish("v1/devices/me/telemetry",myoutput) #topic-v1/devices/me/telemetry      
            
        if data['method'] == 'setValue':
            params = data['params']
            setValue(params)
            client.publish('v1/devices/me/telemetry', json.dumps(button_state), 1)
            
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(ACCESS_TOKEN)
client.connect(THINGSBOARD_HOST,1883,60)

t = Thread(target=publishValue, args=(client,))

try:
    client.loop_start()
    t.start()
    while True:
        pass

except KeyboardInterrupt:
    client.disconnect()
