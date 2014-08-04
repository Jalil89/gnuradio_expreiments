import sys
sys.path.append('../misc')

from simpleMAC import simpleMAC

class receiverMAC(simpleMAC):
    def __init__(self,mac_addr):
        simpleMAC.__init__(self,mac_addr)

    def packetHandler(self,ok,pktno,data):
        print "new ok = %5s  type=PACKET  pktno= %5d  datalen = %4d " % (ok,pktno,len(data)) 