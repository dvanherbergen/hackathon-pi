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

address = 1

data = {}
data['device_id'] = "colruyt-pi"
data['setpoint'] = i.read_register(0, 2)
data['override_control'] = override_control.get(i.read_register(1, 0), "unknown")
data['actuator_type'] = actuator_type.get(i.read_register(3, 0), "unknown")
data['relative_pos'] = i.read_register(4, 2)
data['absolute_pos'] = i.read_register(5, 2)
data['relative_flow'] = i.read_register(6, 2)
data['absolute_flow'] = i.read_long(9, 3)
data['setpoint_absolute_flow'] = i.read_long(13, 3)
data['setpoint_analog'] = i.read_register(15, 2)
data['active_sequence'] = active_sequence.get(i.read_register(16, 0), "unknown")
data['serial'] = str(i.read_register(100, 0)) + "-" + str(i.read_register(101, 0)) + "-" + str(i.read_register(102, 0))
data['firmware'] = i.read_register(103, 0)
data['malfunction'] = i.read_register(104, 0)
data['vmax_1'] = i.read_register(105, 2)
data['vmax_2'] = i.read_register(106, 2)
data['control_mode'] = control_mode.get(i.read_register(116, 0), "unknown")
data['unit_selection_flow'] = unit_selection_flow.get(i.read_register(117, 0), "unknown")
data['setpoint_source'] = setpoint_source.get(i.read_register(118, 0), "unknown")

json_data = json.dumps(data)

print(json_data)


#i.write_register(0, 100, numberOfDecimals=2)

#close full
#i.write_register(1, 1)

# set vmax 1
i.write_register(105, 100, numberOfDecimals=2)

# set vmax 2
i.write_register(106, 100, numberOfDecimals=2)







