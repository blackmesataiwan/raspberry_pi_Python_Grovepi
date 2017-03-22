import time
import grovepi  
import datetime
import json
import os
import QIoT

DHTSensor = 8
    
Sound = 1
Rotary = 0
Piezo = 1
Light = 2

Button = 2
Touch = 3

LED = 4



grovepi.pinMode(Sound,"INPUT")
grovepi.pinMode(Rotary,"INPUT")
grovepi.pinMode(Piezo,"INPUT")
grovepi.pinMode(Light,"INPUT")

grovepi.pinMode(Button,"INPUT")
grovepi.pinMode(Touch,"INPUT")

grovepi.pinMode(LED,"OUTPUT")





client = QIoT.setup('./res/resourceinfo.json', '/ssl/')


""" 
	Receive data of QIoT Suite Lite.
"""

#Setting Subscribe is use id <QIoT.subscribeofid("ID", client)>
#It will return topic name


def on_connect(client, userdata, flags, rc):
    global topic_LED
    print("Connected with result code "+str(rc))
    topic_LED = QIoT.subscribeofid("LED", client)

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    data = json.loads(msg.payload)
    if msg.topic == topic_LED:
    	if int(data['value']) == 1:
    		grovepi.digitalWrite(LED,1)
    	else:
    		grovepi.digitalWrite(LED,0)
    	

client.on_connect = on_connect
client.on_message = on_message


"""
	Send sensor's data to QIoT Suite Lite by Resourcetype.
"""

#It's use "resourcetypename" to sending data.
#QIoT.sendoftype("resourcetypename", value, client)

while True:
	try:	
		t = time.time()
		[temp,humidity] = grovepi.dht(DHTSensor,0)
		QIoT.sendoftype("Temperature", temp, client)
		QIoT.sendoftype("Humidity", humidity, client)

		QIoT.sendoftype("Sound", int(grovepi.analogRead(Sound)/1023*100), client)
		QIoT.sendoftype("Rotary", int(grovepi.analogRead(Rotary)/1023*100), client)
		QIoT.sendoftype("Piezo", 1 if (grovepi.analogRead(Piezo) > 100) else 0 , client)
		QIoT.sendoftype("Light", grovepi.analogRead(Light), client)
		
		QIoT.sendoftype("Button", grovepi.digitalRead(Button), client)
		QIoT.sendoftype("Touch", grovepi.digitalRead(Touch), client)
		time.sleep(1)
	except Exception as e:
		print "IO ERROR"




