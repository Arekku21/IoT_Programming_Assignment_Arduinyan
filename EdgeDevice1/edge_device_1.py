import mysql.connector
import serial
import datetime
import paho.mqtt.client as paho
import os
import json
import paho.mqtt.publish as publish
import schedule
import time
import sys
import random
import paho.mqtt.client as mqtt
from threading import Thread


ACCESS_TOKEN= '21Ee35J5f5NGsVMePtb5'               #Token of your device
THINGSBOARD_HOST="thingsboard.cloud"       #host name
port=1883

device = '/dev/ttyACM0' 
arduino = serial.Serial(device, 9600)

button_state = {"Door":"Open"}

def publishValue(client):
    INTERVAL = 2
        
    while True:
        mydb = mysql.connector.connect(host="localhost",user="pi",password="raspberry",database="gatesensor_db")
        
        while(arduino.in_waiting == 0):
            pass
        
        line = arduino.readline()
        line = line.decode("utf-8")
        
        pieces = line.split(" ")
        
        distance = pieces[0]
        status = pieces[1]
        door = pieces[2]
        
        time = datetime.datetime.now()
        date = time.strftime("%Y-%m-%d %H:%M:%S")
        
        myoutput='{"Distance":' + distance + ', "Status":' + status + ', "Door":' + door + '}'
        
        client.publish("v1/devices/me/telemetry",myoutput) #topic-v1/devices/me/telemetry
        print(myoutput)
        
        with mydb:
            mycursor = mydb.cursor()
            mycursor.execute("INSERT INTO doorsensor (Distance, Status, Door, Date) VALUES (%s,%s,%s,%s)", (distance,status,door,date))
            mydb.commit()
            mycursor.close()
        
        

def read_distance():
    distancevalue = button_state['Door']
    return distancevalue

def setValue(params):
    arduino.write(str("Open").encode())
    
def on_connect(client, userdata, flags, rc):
    client.subscribe('v1/devices/me/rpc/request/+')
    
def on_message(client, userdata, msg):
    if msg.topic.startswith('v1/devices/me/rpc/request/'):
        requestId = msg.topic[len('v1/devices/me/rpc/request/'):len(msg.topic)]
        data = json.loads(msg.payload)
        if data['method'] == 'getValue':
            
            mydb = mysql.connector.connect(host="localhost",user="pi",password="raspberry",database="gatesensor_db")

            line = arduino.readline()
            line = line.decode("utf-8")
            
            pieces = line.split(" ")
            
            distance = pieces[0]
            status = pieces[1]
            door = pieces[2]
            
            time = datetime.datetime.now()
            date = time.strftime("%Y-%m-%d %H:%M:%S")
            
            myoutput='{"Distance":' + distance + ', "Status":' + status + ', "Door":' + door + '}'
            
            client.publish("v1/devices/me/telemetry",myoutput) #topic-v1/devices/me/telemetry
            
            with mydb:
                mycursor = mydb.cursor()
                mycursor.execute("INSERT INTO doorsensor (Distance, Status, Door, Date) VALUES (%s,%s,%s,%s)", (distance,status,door,date))
                mydb.commit()
                mycursor.close()
            
            
        if data['method'] == 'setValue':
            params = data['params']
            setValue(params)
            
            
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
            
        
        

    
    
