from appconfig import AppConfig
from wifi import WiFi
from eink import EInk
from led import Led,LedDummy
from esp32_regs import GetResetCauseText

import time
from machine import deepsleep,reset


def print_message(text=None):
    eink.clear()
    eink.print("*** %s *** Ver. %s" % (cfg.TITLE,cfg.VERSION))
    eink.print("EInk %ix%i" % (cfg.SCR_WIDTH,cfg.SCR_HEIGHT) )
    eink.print("SSID %s" % cfg.AP_SSID)
    eink.print("URL %s" % cfg.URL)
    if (text):
        eink.print("")
        eink.print(text)
    eink.update(True)
    led.blink()

def print_error(text):
    global error_count
    print_message("Error: %s  %i(%i)" % (text,error_count+1,cfg.ERROR_RETRY_COUNT))
    if (error_count>=cfg.ERROR_RETRY_COUNT):
        print("There are too many errors. Reset.")
        reset()
    error_sleep_sec = cfg.ERROR_RETRY_SEC[error_count]
    error_count+=1
    print("Sleep %i sec" % error_sleep_sec)
    time.sleep(error_sleep_sec)
    
    


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
    
    
    errortext = ""
    try:
        rc = wlan.connect()
    except Exception as e:
        errortext = str(e)
        rc=False

   
    if (not rc):
        print_error("WiFi connection failed."+errortext)
        continue
    
    try:
        img = wlan.load()
    except Exception as e:
        print_error("\n  Image load failed.\n  "+str(e)+"\n" )
        continue

    error_count = 0
    assert img!=None
    eink.show(img)
    
    print("Deep sleep %i sec" % (cfg.IMAGE_RELOAD_PERIOD_MS/1000))
    deepsleep(cfg.IMAGE_RELOAD_PERIOD_MS)