from machine import Pin, SPI
import time
from epaper2in9 import EPD
from screenbuffer import Screen
from imagecomparer import ImageComparer




class EInk:
    
    
    def __init__(self,appcfg):
        self.cfg = appcfg
        spi = SPI(  2,
                    baudrate=80000000,
                    polarity=0,
                    phase=0,
                    bits=8,
                    firstbit=0,
                    sck=Pin(appcfg.PIN_CLK),
                    mosi=Pin(appcfg.PIN_DIN),
                    miso=Pin(appcfg.PIN_DOUT))
        
        cs = Pin(appcfg.PIN_CS,Pin.OUT)
        dc = Pin(appcfg.PIN_DC,Pin.OUT)
        rst = Pin(appcfg.PIN_RST,Pin.OUT)
        busy = Pin(appcfg.PIN_BUSY,Pin.IN)
        self.dev = EPD(spi, cs, dc, rst, busy)
        self.dev.init()
        print("EInk init")
        
        self.scr = Screen(appcfg)
        self.cmp = ImageComparer()

        
    def clear(self):
        self.scr.clear()        
        
    def update(self,isforceupdate=False):
        self.show(self.scr.data,isforceupdate)
        
        
    def show(self,data,isforceupdate=False)->bool: 
        isthesame = self.cmp.check(data)
        if (isthesame) and (not isforceupdate):
            print("EInk upadate skipped")
            return False
        self.dev.set_frame_memory(data, 0, 0, self.cfg.SCR_WIDTH, self.cfg.SCR_HEIGHT)
        self.dev.display_frame()
        return True
        
        
    def print(self,text):
        self.scr.print(text)
        
        
        
    def printat(self,text,x,y):
        self.scr.printat(text,x,y)
        
        
        
        
        
