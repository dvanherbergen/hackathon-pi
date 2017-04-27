# Import packages to access ip info
import socket
import fcntl
import struct
import time
import Adafruit_DHT 
import minimalmodbus
import json

moist, temp = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 4)

print moist

