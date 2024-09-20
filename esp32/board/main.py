from appconfig import AppConfig
from wifi import WiFi
from eink import EInk
from led import Led,LedDummy
from esp32_regs import GetResetCauseText

import time
from machine import deepsleep


def print_message(text=None):
    eink.clear()
    eink.print("*** %s *** Ver. %s" % (cfg.TITLE,cfg.VERSION))
    eink.print("EInk %ix%i" % (cfg.SCR_WIDTH,cfg.SCR_HEIGHT) )
    eink.print("SSID %s" % cfg.AP_SSID)
    eink.print("URL %s" % cfg.URL)
    if (text):
        eink.print("")
        eink.print(text)
    eink.update()
    led.blink()

def print_error(text):
    global error_count 
    print_message("Error: %s (%i)" % (text,error_count))
    error_count+=1
    time.sleep(cfg.ERROR_RETRY_SEC)
    


cfg = AppConfig()
#led = Led(cfg.PIN_LED)
led = LedDummy()
wlan = WiFi(cfg,led)
eink = EInk(cfg)

cfg.print()
print("------")

#print_message(GetResetCauseText())
#time.sleep(10)





error_count = 0


while (True):
    
    rc = wlan.connect()
    if (not rc):
        print_error("WiFi connection failed.")
        continue
    
    img = wlan.load()
    if (img):
        eink.show(img)
    else:
        print_error("Image load failed.")
        continue
    

    deepsleep(cfg.IMAGE_RELOAD_PERIOD_MS)




    
    
    
    
