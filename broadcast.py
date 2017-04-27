# Import packages to access ip info
import socket
import fcntl
import struct
import time
import Adafruit_DHT 
import minimalmodbus
import json


# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])



m = minimalmodbus

# Baud Rate : 19200
# MODBUS RTU format : 1-8-N-1

# Data bits 8
m.BYTESIZE = 8
# Parity none
m.PARITY = 'N'
# Stop bits 2
m.STOPBITS = 1
m.TIMEOUT = 0.5 

# 38400 baud
m.BAUDRATE = 19200

#i = m.Instrument('/dev/tty.usbserial-AK04OVSN', 1)



override_control = {
  0: "None",
  1: "Open Sequence 1 (0%)",
  2: "Open Sequence 2 (100%)",
  3: "Close (50%)",
  4: "Vmax Sequence 1",
  5: "Vmax Sequence 2"
}

actuator_type = {
  0: "Unknown",
  1: "Air & Water",
  2: "EPIV/VAV",
  3: "Fire",
  4: "EnergyValve",
  5: "6-way EPIV"
}

active_sequence = {
  0: "Sequence 1 (0...33%)",
  1: "Sequence 2 (67...100%)",
  2: "Dead band (34...66%)"
}

control_mode = {
  0: "Position Control",
  1: "Flow Control"
}

unit_selection_flow = {
  0: "m3/s",
  1: "m3/h",
  2: "l/s",
  3: "l/min",
  4: "l/h",
  5: "gpm",
  6: "cfm"
}

setpoint_source = {
  0: "Analog",
  1: "Bus"
}





# For certificate based connection
client = AWSIoTMQTTClient("colruyt-pi")
client.configureEndpoint("a31v8wvq1ft4tj.iot.eu-west-2.amazonaws.com", 8883)
client.configureCredentials("/home/pi/certs/aws-root-ca.cert", "/home/pi/certs/colruyt-pi-private.key", "/home/pi/certs/colruyt-pi.cert")

client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
client.configureDrainingFrequency(2)  # Draining: 2 Hz
client.configureConnectDisconnectTimeout(10)  # 10 sec
client.configureMQTTOperationTimeout(5)  # 5 sec

client.connect()


def changeValve(client, userdata, message):
  try:
    pos = int(message.payload)
    if (pos >= 0 & pos <= 100):
      print "Setting valve to: %s " % pos
    else:
      print "Invalid valve setting provided : %s " % pos
  except:
    print "Invalid valve setting provided : %s " % message.payload

client.subscribe("colruyt-pi/valve", 1, changeValve)

def main_loop():
	
	#eth0_ip = get_ip_address("eth0")
	#wlan0_ip = get_ip_address("wlan0")
	#print("eth0  : %s" % eth0_ip)
	#print("wlan0 : %s" % wlan0_ip)
	#client.publish("colruyt-pi/ip/eth0", eth0_ip, 0)
  moist, temp = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 4)

  data = {}
  data['device_id'] = "colruyt-pi"

  data['moisture'] = moist
  data['temperature'] = temp
  data['recorded_on'] = time.time()

  json_data = json.dumps(data)
  client.publish("colruyt-pi", json_data, 0)
  print(json_data)

while True:
	main_loop()
	time.sleep(5)

client.disconnect()
