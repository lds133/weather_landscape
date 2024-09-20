import machine 



def GetResetCauseText():

    RTC_CNTL_RESET_STATE_REG = 0x3FF48034
    r = machine.mem32[0x3FF48034]

    PRO = r & 0x3F
    APP = (r >> 6) & 0x3F

    text = "Unknown"

    if PRO==0x01 and APP==0x01: text="Chip Power On Reset"   
    if PRO==0x10 and APP==0x10: text="RWDT System Reset"     
    if PRO==0x0F and APP==0x0F: text="Brown Out Reset"       
    if PRO==0x03 and APP==0x03: text="Software System Reset" 
    if PRO==0x05 and APP==0x05: text="Deep Sleep Reset"      
    if PRO==0x07 and APP==0x07: text="MWDT0 Global Reset"    
    if PRO==0x08 and APP==0x08: text="MWDT1 Global Reset"    
    if PRO==0x09 and APP==0x09: text="RWDT Core Reset"       
    if PRO==0x0B              : text="MWDT0 CPU Reset"       
    if PRO==0x0C              : text="Software CPU Reset"    
    if               APP==0x0B: text="MWDT1 CPU Reset"       
    if               APP==0x0C: text="Software CPU Reset"    
    if PRO==0x0D and APP==0x0D: text="RWDT CPU Reset"        
    if               APP==0x0E: text="PRO CPU Reset"  

    print("Reset cause PRO=0x%02X  APP=0x%02X (%s)" %(PRO,APP,text))
    
    return "%s (%02X,%02X)" % (text,PRO,APP)



