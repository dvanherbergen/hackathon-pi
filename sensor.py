# Import packages to access ip info
import time
import Adafruit_DHT 




def main_loop():
	moist, temp = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 4)
	data_file = open("am2302.data", "w")
	data_file.write(str(temp) + "@" + str(moist))
	data_file.close()
	print "Temperature: %s      Moisture: %s" % (temp, moist)

while True:
	main_loop()
	time.sleep(2)
