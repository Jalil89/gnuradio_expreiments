import struct


class H264Packet:
	UNKNOWN_TYPE = 0
	I_HDR = 1
	P_HDR = 2
	B_HDR = 3
	I_DATA = 4
	P_DATA = 5
	B_DATA = 6

	
	def __init__(self, packet):
		self.type = None
		self.data = None
		if len(packet > 3):
			self.type = struct.unpack('H', packet[0:2])
			self.data = struct.unpack('H', packet[2:])
	
		
	def type(self):
		return self.type
	
	def data(self):
		return self.data