#system
import serial
import mysql.connector
import time
import schedule
import json
import os
import sys
import random

#mqtt
import paho.mqtt.client as paho
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
from threading import Thread

#thingsboard mqtt procedure
ACCESS_TOKEN='2jQrXNE9FTxgKpiYpWrY'         
broker="thingsboard.cloud"       
port=1883

#iot node
device = '/dev/ttyACM0'
arduino = serial.Serial(device,9600)           

#state
feeder_state = {"Feeder":"NotFeeding"}
feeding_mode = "normal"
#function for publishing value
def publishValue(client):
    while True:
        schedule.run_pending()
        #time.sleep(1)
        while(arduino.in_waiting == 0):
            #print("Error Arduino Serial Read")
            pass
        mydb = mysql.connector.connect(host="localhost",user="pi",password="",database="catfeedersensor_db")
        print (mydb)
        
        #read the data from arduino and then turn into string for processing
        arduino_data = arduino.readline()
        sensor_reading = str(arduino_data[0:len(arduino_data)].decode("utf-8"))

        #split the values as per the delimiter
        sensor_reading_list = sensor_reading.split("x")

        #assign the list values into variables
        PIR_sensor_reading = sensor_reading_list[0]
        Photo_sensor_reading = sensor_reading_list[1]
        
        payload="{"
        payload+="\"PIR_sensor_reading\":" + PIR_sensor_reading + ","; 
        payload+="\"Photosensor_reading\":" + Photo_sensor_reading.strip("\r\n"); 
        payload+="}"

        #send data to mqtt telementery thingsboard
        ret = client.publish("v1/devices/me/telemetry",payload) #topic-v1/devices/me/telemetry
        print(payload)
        print("Success \n")
        
        with mydb:
            mycursor = mydb.cursor()
            mycursor.execute("INSERT INTO sensorreadings (PIR_Sensor_Reading, Photo_Sensor_Reading) VALUES (%s,%s)" %(PIR_sensor_reading,Photo_sensor_reading))
            mydb.commit()
            mycursor.close()

def on_connect(client,userdata,flags,rc):
    client.subscribe('v1/devices/me/rpc/request/+')
    
def on_message(client, userdata, msg):
    if msg.topic.startswith('v1/devices/me/rpc/request/'):
        requestId = msg.topic[len('v1/devices/me/rpc/request/'):len(msg.topic)]
        data = json.loads(msg.payload)
        if data['method'] == 'getValue':
            publishValue(client)
        if data['method'] == 'forceDispense':
            params = data['params']
            forceDispense(params)
            feeder_state['feeder'] = 'Feeding'
            client.publish('v1/devices/me/telemetry', json.dumps(feeder_state), 1)
        if data['method'] == 'setDiet':
            global feeding_mode
            if feeding_mode == "normal":
                 
                feeding_mode = "diet"
            else:
                
                feeding_mode = "normal"
                
            params = data['params']
            forceDispense(params)
            client.publish('v1/devices/me/telemetry', json.dumps(feeder_state), 1)
def forceDispense(params):
    
    #read the data from arduino and then turn into string for processing
    arduino_data = arduino.readline()
    sensor_reading = str(arduino_data[0:len(arduino_data)].decode("utf-8"))

    #split the values as per the delimiter
    sensor_reading_list = sensor_reading.split("x")

    #assign the list values into variables
    PIR_sensor_reading = sensor_reading_list[0]
    Photo_sensor_reading = sensor_reading_list[1]
    
    if params == "schedfeed":
        print("\nSCHED FEED\n")
        print(PIR_sensor_reading + Photo_sensor_reading)
        if int(PIR_sensor_reading) > 0 and int(Photo_sensor_reading) > 70:
            if feeding_mode == "normal":
                arduino.write(b"1")
                feeder_state['feeder'] = 'NotFeeding'
            else:
                arduino.write(b"3")
                feeder_state['feeder'] = 'NotFeeding'
    
    if params == "feed":
        if feeding_mode == "normal":
            arduino.write(b"1")
            feeder_state['feeder'] = 'NotFeeding'
        else:
            arduino.write(b"3")
            feeder_state['feeder'] = 'NotFeeding'
    

#client mqtt
client= paho.Client("control1")                    
#client.on_publish = on_publish
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(ACCESS_TOKEN)               
client.connect(broker,port,keepalive=60)

t = Thread(target=publishValue, args=(client,))

try:
    schedule.every(10).seconds.do(forceDispense,"schedfeed")
    client.loop_start()
    t.start()
    while True:
        pass

except KeyboardInterrupt:
    client.disconnect()



    
        

    
  
        

