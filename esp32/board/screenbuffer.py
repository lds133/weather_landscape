
import bitmapfont





def bit_not(n, numbits=8):
    return (1 << numbits) - 1 - n

class Screen:


    def __init__(self,appcfg):
        print("Screen init")       
        self.BYTES_PER_LINE = int(appcfg.SCR_WIDTH / 8)
        self.bufsize = int(appcfg.SCR_WIDTH*appcfg.SCR_HEIGHT/8)
        self.clear()
        #self.bf = bitmapfont.BitmapFont(appcfg.SCR_WIDTH , appcfg.SCR_HEIGHT, self.set_pixel_v)
        self.bf = bitmapfont.BitmapFont(appcfg.SCR_HEIGHT, appcfg.SCR_WIDTH , self.set_pixel_h) 
        self.bf.init()
        

    def set_pixel_v(self,x,y):
        pos = self.BYTES_PER_LINE*y
        pos+= int(x / 8)
        mask = 1 << (7-(x % 8))
        if (pos<len(self.scrbuf)):
            self.scrbuf[pos] &= bit_not(mask)
        
    def set_pixel_h(self,x,y):
        pos = self.BYTES_PER_LINE*x + (self.BYTES_PER_LINE-1)
        pos -=int( y/8 )
        mask = 1 << (y % 8)
        if (pos<len(self.scrbuf)):
            self.scrbuf[pos] &= bit_not(mask)
        #self.scrbuf[pos] = 0
        
        
        
        
    def print(self,text):
         print("Screen text:",text)
         lines = text.split('\n')
         for line in lines:
             self.bf.text(line, self.x, self.y)
             self.x=0#self.bf.width(text)
             self.y+=self.bf.get_font_height()+1
         
         
        
        
    def printat(self,text,x,y):
         print("Screen text:",text)
         self.bf.text(text, x, y)
         
         
         
         
    def clear(self):
        self.scrbuf = bytearray([0xFF] * self.bufsize  )
        self.x = 0
        self.y = 0
        print("Screen clear")       
        
        
    @property        
    def data(self):
        return self.scrbuf 
        
        