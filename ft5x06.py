import smbus
import uinput
import pprint
import sys

device = uinput.Device([
        uinput.BTN_LEFT,
        uinput.BTN_RIGHT,
        uinput.REL_X,
        uinput.REL_Y,
        ])

bus = smbus.SMBus(0)


def ft():
	#bus.write_byte_data(0x38, 0x38, 30)
	x = bus.read_i2c_block_data(0x38,0, 8 )
	print(x)
	device.emit(uinput.REL_X, (x[3]/255))
	device.emit(uinput.REL_Y, (x[6]/255))
	return
def main():
	bl = True
	x = bus.read_i2c_block_data(0x38,0, 30 )
	print(x)
        if x[2] > 0 & bl == True:
		x_ = x[3]/150
		y = x[6]/150
                bl = False
	elif x[2] > 0 & bl == False:
		x_ = x[3]*-1/150
		y = x[6]*-1/150
		bl = True
	else:
		x_ = 0
		y = 0	
		bl = True

	events = (
        	uinput.ABS_X + (0, 255, 0, 0),
        	uinput.ABS_Y + (0, 255, 0, 0),
       	 )
		#with uinput.Device(events) as device:
        	#for i in range(20):
            	#syn=False to emit an "atomic" (5, 5) event.
       	device.emit(uinput.REL_X, x_, syn=False)
       	device.emit(uinput.REL_Y, y)
	print(x[4],x[6])
	print(x_, y)

class TouchMessage:
	def __init__(self, buf):
		self.n_fingers = buf[2]
		self.flags = (buf[3] >> 5) & (1 | 2 | 4)
        	coord0 = ((buf[3] & 7) << 8) | buf[4]
		coord1 = ((buf[5] & 15) << 8) | buf[6]  
		self.coords = (coord0, coord1)
	def __repr__(self):
		return pprint.pformat(dict(
			n_fingers=self.n_fingers,
			flags='{:03b}'.format(self.flags),
			coords=self.coords))

def touchscreen_stream():
	while True:
		yield TouchMessage(bus.read_i2c_block_data(0x38, 0, 8))

try:
	for state in touchscreen_stream():
		sys.stdout.write('\r{}'.format(state).ljust(79))
		sys.stdout.flush()
except KeyboardInterrupt:
	pass
finally:
	print()
