import sys,time,math,random
sys.path.append("../misc/")

from extractH264Header import H264Packet



CWmin = {I_HDR:7,
         P_HDR:7,
         B_HDR:7,
         I_DATA:7,
         P_DATA:15,
         B_DATA:15,
         UNKNOWN_TYPE:31}

CWmax = {I_HDR:15,
         P_HDR:15,
         B_HDR:15,
         I_DATA:15,
         P_DATA:31,
         B_DATA:31,
         UNKNOWN_TYPE:1023}

RT = {I_HDR:8,
         P_HDR:8,
         B_HDR:8,
         I_DATA:8,
         P_DATA:4,
         B_DATA:4,
         UNKNOWN_TYPE:4}



class MacParamRef(object):
    def __init__(self,type):
        self.t_attempts = 0
        self.type = type
        self.maxCW = CWmax[type]
        self.minCW = CWmin[type]
        self.CW = self.minCW + 1
        self.RT = RT[type]
        
    def backoff(self):
        cw = float(random.randint(self.minCW,self.CW))
        time.sleep(cw/1000)
        if self.CW < self.maxCW:
            self.CW = self.CW*2
        
        
    def initialize(self,attempts):
        cw = (self.minCW*math.pow(2,attempts)) - 1
        if cw<self.maxCW:
            self.CW = cw
        
    def RT(self):
        return self.RT
                   

             
        
        