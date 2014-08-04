import sys
sys.path.append('../misc')

from simpleMAC import simpleMAC


class senderMAC(simpleMAC):
    def __init__(self,mac_addr):
        simpleMAC.__init__(self,mac_addr)
        
    def Send(self,payload,retcount):
        print '.',
        self.sendPacket(payload)
        return self.wait_delivery_status()
        

    def packetHandler(self,ok,pktno,data):
        print "new ok = %5s  type=PACKET  pktno= %5d  datalen = %4d " % (ok,pktno,len(data)) 