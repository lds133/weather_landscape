from p_weather.configuration import WLBaseSettings

class WLConfig_BW(WLBaseSettings):
    TITLE = "BW"
    WORK_DIR = "tmp"
    OUT_FILENAME = "landscape_wb"
    OUT_FILEEXT = ".bmp"
    TEMPLATE_FILENAME = "p_weather/template_wb.bmp"
    SPRITES_DIR="p_weather/sprite"
    POSTPROCESS_INVERT = False
    POSTPROCESS_EINKFLIP = False    
    
class WLConfig_EINK(WLConfig_BW):
    TITLE = "BW EINK"
    OUT_FILENAME = "landscape_eink"
    POSTPROCESS_INVERT = False   
    POSTPROCESS_EINKFLIP = True    
    
    
    
class WLConfig_BWI(WLConfig_BW):
    TITLE = "BW inverted"
    OUT_FILENAME = "landscape_wbi"
    POSTPROCESS_INVERT = True
    POSTPROCESS_EINKFLIP = False


    
class WLConfig_RGB_White(WLBaseSettings):    
    TITLE = "Color, white BG"
    WORK_DIR = "tmp"    
    OUT_FILENAME = "landscape_rgb_w"
    OUT_FILEEXT = ".png"    
    SPRITES_DIR="p_weather/sprite_rgb"
    TEMPLATE_FILENAME = "p_weather/template_rgb.bmp"

    POSTPROCESS_INVERT = False
    POSTPROCESS_EINKFLIP = False
    SPRITES_MODE = WLBaseSettings.SPRITES_MODE_RGB


    COLOR_SOIL = (148, 82, 1)
    COLOR_SMOKE = (127,127,127) 
    COLOR_BG = (255,255,255)
    COLOR_FG = (0,0,0)    
    COLOR_RAIN = (10, 100, 148)
    COLOR_SNOW = (194, 194, 194)
    
    
class WLConfig_RGB_Black(WLConfig_RGB_White):    
    TITLE = "Color, black BG"
    OUT_FILENAME = "landscape_rgb_b"

    COLOR_SOIL = (148, 82, 1)
    COLOR_SMOKE = (127,127,127) 
    COLOR_BG = (0,0,0)
    COLOR_FG =     (255,255,255)
    COLOR_RAIN = (122, 213, 255)
    COLOR_SNOW = (255,255,255)    

# ── Fahrenheit variants ──────────────────────────────────────────────────

class WLConfig_BW_F(WLConfig_BW):
    TITLE = "BW °F"
    OUT_FILENAME = "landscape_wb_f"
    TEMPUNITS_MODE = 1

class WLConfig_EINK_F(WLConfig_EINK):
    TITLE = "BW EINK °F"
    OUT_FILENAME = "landscape_eink_f"
    TEMPUNITS_MODE = 1

class WLConfig_BWI_F(WLConfig_BWI):
    TITLE = "BW inverted °F"
    OUT_FILENAME = "landscape_wbi_f"
    TEMPUNITS_MODE = 1

class WLConfig_RGB_White_F(WLConfig_RGB_White):
    TITLE = "Color °F, white BG"
    OUT_FILENAME = "landscape_rgb_w_f"
    TEMPUNITS_MODE = 1

class WLConfig_RGB_Black_F(WLConfig_RGB_Black):
    TITLE = "Color °F, black BG"
    OUT_FILENAME = "landscape_rgb_b_f"
    TEMPUNITS_MODE = 1