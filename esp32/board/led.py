from machine import Pin, Timer
import time

class LedDummy():
    
    def __init__(self):
        pass
        
    def off(self):
        pass

    def on(self):
        pass

    def blink(self,n=None):
        pass
    
    def flash(self,n=None):
        pass

    def blink_n(self,n,delay):
        pass







class Led():
    
    
    def __init__(self,ledpin):
        self.led = Pin(ledpin, Pin.OUT)
        self.timer = Timer(0)
        self.toggle = False
        self.off()
        
    def off(self):
        self.timer.deinit()
        self.led.value(0)
        self.toggle = False
        

    def on(self):
        self.timer.deinit()
        self.led.value(1)
        self.toggle = True


    def blink(self,n=None):
        if (n==None):
            self.timer.init(freq=2, mode=Timer.PERIODIC, callback=self.blinkproc)
        else:
            self.blink_n(n,0.5)
    
    def flash(self,n=None):
        if (n==None):
            self.timer.init(freq=10, mode=Timer.PERIODIC, callback=self.blinkproc)
        else:
            self.blink_n(n,0.1)

    def blink_n(self,n,delay):
        self.off()
        for i in range(n):
            self.led.value(1)
            time.sleep(delay)
            self.led.value(0)
            time.sleep(delay)


    def blinkproc(self,timer):
        self.led.value( 1 if self.toggle else 0)
        self.toggle = not self.toggle


