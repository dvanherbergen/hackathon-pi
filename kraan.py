import minimalmodbus

m = minimalmodbus

# Baud Rate : 19200
# MODBUS RTU format : 1-8-N-1

# Start bit	1
# always 1?

# Data bits	8
m.BYTESIZE = 8

# Parity none
m.PARITY = 'N'

# Stop bits 2
m.STOPBITS = 1

m.TIMEOUT = 0.5 

# 38400 baud

m.BAUDRATE = 19200


i = m.Instrument('/dev/tty.usbserial-AK04OVSN', 1)
#i.debug = True

print i


#	try:

for j in range(0,15):
	value = i.read_register(j, 1)
	print("Register %s : %s" % (j , value))

i.write_register(1, 10)