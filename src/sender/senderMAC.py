import sys
sys.path.append('../misc')

from simpleMAC import simpleMAC
from H264Packet import H264Packet
from mac_parameters_ref import MacParamRef



class senderMAC(simpleMAC):
    FRM_HDR_RET_COUNT = 8
    FRM_DATA_RET_COUNT = 4
    
    def __init__(self,mac_addr):
        simpleMAC.__init__(self,mac_addr)
        self.macpars = { H264Packet.I_HDR: MacParamRef(H264Packet.I_HDR),
                         H264Packet.I_DATA: MacParamRef(H264Packet.I_DATA),
                         H264Packet.P_HDR: MacParamRef(H264Packet.P_HDR),
                         H264Packet.P_DATA: MacParamRef(H264Packet,P_DATA),
                         H264Packet.B_HDR: MacParamRef(H264Packet.B_HDR),
                         H264Packet.B_DATA: MacParamRef(H264Packet.B_DATA),
                         H264Packet.UNKNOWN: MacParamRef(H264Packet.UNKNOWN)
                        }
        
    def Send(self,payload):
        packet = H264Packet(payload)
        print packet.type
        cw = self.macpars[packet.type]
        retcount = cw.RT()
            
 
        
        #Send the packets and get delivery status
        # TODO: add the contention window backoff
        for i in range(retcount):
            self.sendPacket(packet.serialize())
            packet_delivered = self.wait_delivery_status()
            if packet_delivered:
                cw.initialize(i)
                break
            else:
                cw.backoff()
                    
                 
        

    def packetHandler(self,ok,pktno,data):
        print "new ok = %5s  type=PACKET  pktno= %5d  datalen = %4d " % (ok,pktno,len(data)) 