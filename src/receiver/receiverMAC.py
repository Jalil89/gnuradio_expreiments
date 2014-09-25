import sys,time
sys.path.append('../misc')

from simpleMAC import simpleMAC
from H264Packet import H264Packet

class receiverMAC(simpleMAC):
    def __init__(self,mac_addr,tofile):
        simpleMAC.__init__(self,mac_addr)
        self.f = open(tofile,"w")
        self.lastpktno = 0
        
    def sendAck(self,pktno):
        time.sleep(0.1)
        print "Sending ack"
        simpleMAC.sendAck(self,pktno)

    def packetHandler(self,ok,pktno,data):
        packet = H264Packet(data)
        print "new ok = %5s  type=PACKET frametype=%4d pktno= %5d  datalen = %4d " % (ok,packet.type,pktno,len(data))
        if ok: #packet is received without any bit error
            self.sendAck(pktno)
            if pktno > self.lastpktno:
                self.f.write(packet.data)
                self.lastpktno = pktno
        else:
            # We tolerate bit errors for frame packets but not header packets
            if packet.type not in [H264Packet.I_HDR, H264Packet.B_HDR, H264Packet.P_HDR, UNKNOWN_TYPE]:
                self.sendAck(pktno)
                if pktno > self.lastpktno:
                    self.f.write(packet.data)
                    self.lastpktno = pktno
                 
            
         