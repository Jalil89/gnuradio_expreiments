import struct
from threading import Timer
# from current dir
from simple_lock import SimpleLock

class simpleMAC:
    T_ACK = 1
    T_PACKET = 2 
    
    
    def __init__(self,  mac_addr):
        self.pktno = 0 #enumerate sent packets
        self.mutex = SimpleLock()
        self.timeout = 0 # seconds
        self.packet_delivered = False
        self.tb = None
        if len(mac_addr)!=len('xx:xx:xx:xx:xx:xx'):
            print 'malformed Mac address'
        self.MAC_ADDR = mac_addr
        #self.mutex.lock()
        
        
    def set_tb(self,tb):
        self.tb = tb
        
    def __timeout(self,m):
        print m
        self.mutex.unlock()
    
    def __set_timeout(self):
        Timer(self.timeout,self.__timeout,args=["here"]).start()
        
    def wait_delivery_status(self):
        # it function can only return if mutex will be unlocked 
        # by reply message handler or a timeout
        self.__set_timeout()
        self.mutex.lock()
        if self.packet_delivered:
            self.pktno = self.pktno + 1
            self.packet_delivered = True
        return self.packet_delivered
    
    def __makeHeader(self):
        return struct.pack('!H',simpleMAC.T_PACKET) + struct.pack('!H',self.pktno)+self.MAC_ADDR
        
    
    def __makeFrame(self,payload):
        return self.__makeHeader() + payload
    
    def sendPacket(self,payload):
        self.packet_delivered = False
        frame = self.__makeFrame(payload)
        self.tb.send_pkt(frame)
    
    def sendAck(self,pktno):
        ack = struct.pack('!H',simpleMAC.T_ACK)+ struct.pack('!H',pktno)
        self.tb.send_pkt(ack)
        
    
    def packetHandler(self,ok,pktno,data):
        print "ok = %5s  type=PACKET  pktno= %5d  datalen = %4d " % (ok,pktno,len(data))
        
    def handleAck(self,pktno):
        if pktno == self.pktno:
            self.packet_delivered = True
            if mutex.is_locked():
                mutex.unlock()
            
    
    def rx_callback(self,ok, frame):
            try:
                maclen = len('xx:xx:xx:xx:xx:xx')
                (frametype,) = struct.unpack('!H',frame[0:2])
                (pktno,) = struct.unpack('!H', frame[2:4])
                if frametype == simpleMAC.T_ACK:
                    self.handleAck(pktno)
                elif frametype == simpleMAC.T_PACKET:
                    macAddr = frame[4:(4+maclen)]
                    data = frame[(4+maclen):]
                    if macAddr == self.MAC_ADDR:
                        self.packetHandler(ok,pktno,data)
            except: 
                print "struct exception\n"               
            
    
    
            
            
            