import struct


class H264Packet:
	UNKNOWN_TYPE, I_HDR, P_HDR, B_HDR, I_DATA, P_DATA, B_DATA = range(7)

	def __init__(self, packet):
		self.packet = packet
		self.type = None
		self.data = None
		if len(packet) > 3:
			(self.type,) = struct.unpack('H', packet[0:2])
			self.data = packet[2:]
	
	def serialize(self):
		return self.packet 
		
	def type(self):
		return self.type
	
	def data(self):
		return self.data