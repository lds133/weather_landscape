




import os
from PIL import Image


from p_weather.openweathermap import OpenWeatherMap
from p_weather.sprites import Sprites
from p_weather.draw_weather import DrawWeather


class WeatherLandscape:


    OWM_KEY = None # your OpenWeather API key

    # Warsaw
    OWM_LAT = 52.196136
    OWM_LON = 21.007963



    TMP_DIR = "tmp"
    OUT_FILENAME = "test_"
    OUT_FILEEXT = ".bmp"
    TEMPLATE_FILENAME = "p_weather/template.bmp"
    SPRITES_DIR="p_weather/sprite"
    DRAWOFFSET = 65


    def __init__(self):
        assert self.OWM_KEY!=None, "Set OWM_KEY variable to your OpenWeather API key"
        pass




    def MakeImage(self)->Image:
        owm = OpenWeatherMap(self.OWM_KEY,self.OWM_LAT,self.OWM_LON,self.TMP_DIR)
        owm.FromAuto()

        img = Image.open(self.TEMPLATE_FILENAME)

        spr = Sprites(self.SPRITES_DIR,img)

        art = DrawWeather(img,spr)
        art.Draw(self.DRAWOFFSET,owm)

        return img



    def SaveImage(self)->str:
        img = self.MakeImage() 
        placekey = OpenWeatherMap.MakePlaceKey(self.OWM_LAT,self.OWM_LON)
        outfilepath = self.TmpFilePath(self.OUT_FILENAME+placekey+self.OUT_FILEEXT)
        img.save(outfilepath) 
        return outfilepath
        
        

    def TmpFilePath(self,filename):
        return os.path.join(self.TMP_DIR,filename)