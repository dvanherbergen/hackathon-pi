# TODO : concurrency issues..


# Import packages to access ip info
import socket
import fcntl
import struct
import time
import Adafruit_DHT 
import json


# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


# For certificate based connection
client = AWSIoTMQTTClient("colruyt-pi")
client.configureEndpoint("a31v8wvq1ft4tj.iot.eu-west-2.amazonaws.com", 8883)
client.configureCredentials("/home/pi/certs/aws-root-ca.cert", "/home/pi/certs/colruyt-pi-private.key", "/home/pi/certs/colruyt-pi.cert")

client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
client.configureDrainingFrequency(2)  # Draining: 2 Hz
client.configureConnectDisconnectTimeout(10)  # 10 sec
client.configureMQTTOperationTimeout(5)  # 5 sec

client.connect()

def main_loop():
	
  data = {}

  moist, temp = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 4)

  print "Reading valve data..."
  data['device_id'] = "colruyt-pi2"
  data['temperature'] = temp
  data['moisture'] = moist

  json_data = json.dumps(data)
  print(json_data)

  client.publish("colruyt-pi/temp", json_data, 0)
  print "_______________"

while True:
	main_loop()
	time.sleep(2)

client.disconnect()
