import time
import sys  
#import websocket
import datetime
import paho.mqtt.client as mqtt
import json
import os
import ssl, socket

topic_pub = "com/qnap/rajah/pot"


#vals = ""
"""
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
"""
"""
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
"""
def setup(resfile, sslpath):
	global HOST, PORT, USER_NAME, USER_PASS, CLIENT_ID, PRIVATE_CERT, CLIENT_CERT, CA_CERT, RES_DATA
	with open(resfile, 'r') as f:
		data = f.read()
		RES_DATA = json.loads(data)
		HOST = str(RES_DATA['host'][0])
		PORT = int(RES_DATA['port'])
		USER_NAME = str(RES_DATA['username'])
		USER_PASS = str(RES_DATA['password'])
		CLIENT_ID = str(RES_DATA['clientId'])
	f.close()

	print "HOST : " + HOST
	print "PORT : " + str(PORT)
	#deal with file path

	client = mqtt.Client(client_id=CLIENT_ID)
	#client.on_connect = on_connect
	#client.on_message = on_message

	try:
		arr_KEY = RES_DATA['privateCert'].split('/')
		if (len(arr_KEY) > 0) :
			PRIVATE_CERT = os.getcwd() + sslpath + arr_KEY[len(arr_KEY)-1]

		arr_CERT = RES_DATA['clientCert'].split('/')
		if (len(arr_CERT) > 0) :
			CLIENT_CERT = os.getcwd() + sslpath + arr_CERT[len(arr_CERT)-1]

		arr_CA = RES_DATA['caCert'].split('/')
		if (len(arr_CA) > 0) :
			CA_CERT = os.getcwd() + sslpath + arr_CA[len(arr_CA)-1]
		# f.close()
		print "CLIENT_CERT path :" + str(CLIENT_CERT)

		print "PRIVATE_CERT exists or not :" + str(os.path.exists(PRIVATE_CERT))

		# client.tls_set(ca_certs=str(CA_CERT), certfile=str(CLIENT_CERT), keyfile=str(PRIVATE_CERT), tls_version=ssl.SSLv23)
		client.tls_set(ca_certs=str(CA_CERT), certfile=str(CLIENT_CERT), keyfile=str(PRIVATE_CERT))
		client.tls_insecure_set(True)
	except Exception as e:
		print "Use MQTT"
		
	print "USER_NAME : " + USER_NAME + " USER_PASS : " + USER_PASS
	client.username_pw_set(username=USER_NAME, password=USER_PASS)
	print "finish setup"
	try:
		client.connect(host=HOST, port=PORT, keepalive=60)
	except Exception as e:
		print "Error occurred while trying to connect to QIoT Suite broker. Reason : " + str(e.args)
		sys.exit(e)

	client.loop_start()

	return client

def sendoftype(typename, invalue, clobj):
	resources = RES_DATA['resources']
	for res in resources:
		if (typename == str(res["resourcetypename"])) :
			vals = "{\"value\":"+ str(invalue) +"}"
			print "NOW TOPIC_NAME :" + str(res["topic"]) + " MESSAGE : " + str(vals)
			clobj.publish(str(res["topic"]), vals)

def subscribeofid(id_name, clobj):
	resources = RES_DATA['resources']
	for res in resources:
		if (id_name == str(res["resourceid"])) :
			clobj.subscribe(str(res["topic"]))
			print "add subscribe :" + str(res["topic"])
			return str(res["topic"])