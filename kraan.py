import minimalmodbus
import json


m = minimalmodbus

# Baud Rate : 19200
# MODBUS RTU format : 1-8-N-1

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

address = 1

data = {}
data['device_id'] = "colruyt-pi"
data['setpoint'] = i.read_register(0, 2)
data['override_control'] = i.read_register(1, 0)
data['actuator_type'] = i.read_register(3, 0)
data['relative_pos'] = i.read_register(4, 2)
data['absolute_pos'] = i.read_register(5, 2)
data['relative_flow'] = i.read_register(6, 2)
data['absolute_flow'] = i.read_long(9, 3)
data['setpoint_absolute_flow'] = i.read_long(13, 3)
data['setpoint_analog'] = i.read_register(15, 2)
data['active_sequence'] = i.read_register(16, 0)
data['serie_num_part_1'] = i.read_register(100, 0)
data['serie_num_part_2'] = i.read_register(101, 0)
data['serie_num_part_4'] = i.read_register(102, 0)
data['firmware'] = i.read_register(103, 0)
data['malfunction'] = i.read_register(104, 0)
data['vmax_1'] = i.read_register(105, 3)
data['vmax_2'] = i.read_register(106, 3)
data['control_mode'] = i.read_register(116, 0)
data['unit_selection_flow'] = i.read_register(117, 0)
data['setpoint_source'] = i.read_register(118, 0)

json_data = json.dumps(data)

print(json_data)


#i.write_register(1, 10)