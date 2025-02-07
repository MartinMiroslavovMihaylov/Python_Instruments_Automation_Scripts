# version: 1.0.0 2024/11/28

from NovoptelUSB import NovoptelUSB
from NovoptelTCP import NovoptelTCP

import numpy as np 

class controlmode:
    #def __init__(self, detector, gradtype, reference, sensitive, apdcontrol):
    detector = 0
    gradtype = 0
    reference = 0
    sensitive = 0
    apdcontrol = 0



class LU1000():
    
    n = None
    
    def __init__(self, target='192.168.1.100'):
        if (target=='USB'):
            self.n = NovoptelUSB()
            if self.n.DEVNO<0:
                self.n = None
        else:
            self.n = NovoptelTCP(target, port=5025)
        

    def close(self):
        self.n.close()
        del(self.n)
        
        
    #######################    
    # Basic communication #
    #######################
        
    def read(self, addr: int):
        res = self.n.read(addr)
        return res
    
    def readram(self, startaddr: int, numaddr: int):
        res = self.n.readbuffer(startaddr, numaddr)
        return res
        
    def write(self, addr: int, data: int):
        self.n.write(addr, data)
        
        
     
    ###########################    
    # General instrument data #
    ###########################

    def getfirmware(self): # as string
        return hex(self.n.read(84))

    def getserialnumber(self): # as integer
        return self.n.read(91)

    def getmoduletype(self): # as string
         str="";
         for ii in range(16):
            dummy = self.n.read(96+ii)
            str += chr(dummy >> 8)
            str += chr(dummy & 0xFF)

         return str

    def gettemperature(self): # as double
        return self.n.read(181)/16

    def getnrofwlenbands(self): # as integer
        return self.n.read(190)

    def getoptfrequency(self): # in THz
        minfreq = self.n.read(193)/2**7
        maxfreq = self.n.read(192)/2**7
        steps = self.n.read(194)
        stepsize = (maxfreq-minfreq)/steps
        index = self.n.read(25)
        freq = minfreq+stepsize*index
        return freq

    def setoptfrequency(self, freq): # in THz
         minfreq = self.n.read(193)/2**7
         maxfreq = self.n.read(192)/2**7
         steps = self.n.read(194)
         stepsize = (maxfreq-minfreq)/steps
         index = round((freq-minfreq)/stepsize)
         if (index>=0) & (index<=steps):
            self.n.write(25, index)
         else:
            print("'Freq. exceeds range!")

    def setposition(self, wp, position): # as integer 0..2^16-1
         #0: HWP
         #1..6: QWP0..QWP5
         self.n.write(40+wp, round(position))

    def getposition(self, wp): # as integer 0..2^16-1
         #0: HWP
         #1..6: QWP0..QWP5
         return self.n.read(40+wp)


    def setspeed(self, wp, speed): # nominal speed in rad/s
         #0: HWP
         #1..6: QWP0..QWP5
         self.n.write(10+2*wp, 0) # clear MSB register first to avoid overflow
         
         if wp==0: # HWP
            speed = min(20000000, speed) # 20 Mrad/s max
            speed_fpga = round(speed/10)
         else:
            speed = min(2000000, speed) # 2 Mrad/s max
            speed_fpga = round(speed*100)
         
         #print(speed_fpga)
         self.n.write(9+2*wp, speed_fpga & 0xFFFF) # LSB
         self.n.write(10+2*wp, speed_fpga >> 16) # MSB

    def getspeed(self, wp): # nominal speed in rad/s
         #0: HWP
         #1..6: QWP0..QWP5
         r = self.n.read(10+2*wp)*2**16 + self.n.read(9+2*wp)
         if wp==0: # HWP
            r = r*10
         else:
            r = r/100

         return r
    
    def setrotation(self, wp, backw_en):
        #0: HWP
        #1..6: QWP0..QWP5
        #0, 2: STOP
        #1, FORWARD
        #3, BACKWARD
        self.n.write(wp, backw_en)
      
    def setrotation_all(self, backw_en):
        #backw_en is an array of 7 values for 7 waveplates
        val = 0
        for x in backw_en:
            val = (val<<2) + x
            #print(x)
        
        self.n.write(7, val)
        #print(hex(val))
        
        
        
    ###########################    
    #     SOP Tracking        #
    ###########################
    def getcontrolmode(self):
        
        dummy = self.n.read(347)
        
        mode = controlmode()
        
        mode.detector   = dummy & 0x03
        mode.gradtype   = (dummy & 0x04) >> 2
        mode.reference  = (dummy & 0x08) >> 3
        mode.sensitive  = (dummy & 0x30) >> 4
        mode.apdcontrol = (dummy & 0x40) >> 6
        return mode
    
    def setcontrolmode(self, mode):
        self.n.write(347, mode.apdcontrol*2**6 + mode.sensitive*2**4 + mode.reference*2**3 + mode.gradtype*2**2 + mode.detector)
      
        
    def setdetectormode(self, det):
        mode = self.getcontrolmode()
        mode.detector = det
        self.setcontrolmode(mode)
      
      
      ###########################    
      #     PDL measurement     #
      # requires tracking option with optical feedback and fw>=1227
      ###########################
      
    def set_pdl_ext_conf(self, meas_exp, niter):
        # default:           niter = 150; meas_exp = 15
        # fast measurement:  niter = 100; meas_exp = 12
        self.n.write(335, meas_exp*2**11 + niter)
      
    def set_pdl_ext_enable(self, en, ref, pdltype):
        
        if en==1:
            mode = self.getcontrolmode()
            if pdltype=="HIGH":
                mode.sensitive = 3
                DITH = 4
                ATE = 4
            elif pdltype=="LOW":
                DITH = 7
                ATE = 5
            else:
                print("Argument 3 (pdltype) must either be \"LOW\" or \"HIGH\"")
                return
            
            self.n.write(344, 31) # feedback signal delay
            self.n.write(343, ATE) # averaging time exponent
            self.n.write(345, DITH) # dithering amplitude
            
            self.n.write(340, 6) # set tracking mode and enable pdl_ext
            
            mode.gradtype = 1
            self.setcontrolmode(mode)
            
            
        else:
            dummy = self.n.read(340)
            self.n.write(340, dummy & 0xfb) # disable pdl_ext but leave EPS in tracking mode
                
      
    def getpdl_ext(self, withref):
        maxint    = self.n.read(370)   # this latches registers 371 and 372 and locks registers 370 to 372
        maxintref = self.n.read(371)
        bsreg  = self.n.read(372)    # this releases registers 370 to 372
        bs     = bsreg & 0xFF
        bsref  = bsreg >> 8
        maxint    = maxint / 2**bs
        maxintref = maxintref / 2**bsref
        
        minint    = self.n.read(373)  # this latches registers 374 and 375 and locks registers 373 to 375
        minintref = self.n.read(374);
        bsreg = self.n.read(375)     # this releases registers 373 to 375
        bs    = bsreg & 0xFF
        bsref = bsreg >> 8
        minint    = minint / 2**bs
        minintref = minintref / 2**bsref
        
        if withref==0:
            LL  = 1
            HL  = minint/maxint
        else:
            HL = minint/minintref
            LL = maxint/maxintref
            
        ML = (HL+LL)/2
        ML_dB  = -10*np.log10(ML)
        HL_dB  = -10*np.log10(HL)
        LL_dB  = -10*np.log10(LL)
        PDL_dB = HL_dB-LL_dB
        
        return(PDL_dB, ML_dB, HL_dB, LL_dB)
        

        
        
        
        
        
        return