import os
import time
import json
import datetime
from urllib.request import urlopen



class OpenWeatherMapSettings():

    TEMP_UNITS_CELSIUS = 0 
    TEMP_UNITS_FAHRENHEIT = 1
    PRESSURE_RAIN_HPA = 980
    PRESSURE_FAIR_HPA = 1040


    def __init__(self):
        self.OWM_KEY = None
        self.OWM_LAT = None
        self.OWM_LON = None
        self.rootdir = ''
        self.TEMPUNITS_MODE = 0
        self.PRESSURE_MIN = self.PRESSURE_RAIN_HPA
        self.PRESSURE_MAX = self.PRESSURE_FAIR_HPA


    @staticmethod
    def Fill(obj,rootdir:str):
        s = OpenWeatherMapSettings()
        s.rootdir = rootdir
        print("Settings:")
        for key in obj.__dict__.keys():
            if not key.startswith('__'):
                if key.upper() == key:
                    val = obj.__dict__[key]
                    setattr(s, key, val)
                    if (key=='OWM_KEY'):
                        print('  ','OWM_KEY updated')
                    else:
                        print('  ',key,'=',val)
                else:
                    print('  ',key,'ignored')
        return s

        
    @property
    def IsCelsius(self):
        return self.TEMPUNITS_MODE!=self.TEMP_UNITS_FAHRENHEIT



class WeatherInfo():

    KTOC = 273.15

    Thunderstorm = 2
    Drizzle = 3
    Rain =5
    Snow=6
    Atmosphere=7
    Clouds =8

    FORECAST_PERIOD_HOURS = 3


    def toCelsius(self,kelvin:float)->float:
        return kelvin - self.KTOC
        
    def toFahrenheit(self,kelvin:float)->float:
        return (kelvin - self.KTOC) * 1.8 + 32
        

    @property
    def PrintableTemperature(self):
        return self.temp if self.iscelsius else self.temp_fahrenheit

    @property
    def IsCelsius(self)->bool:
        return self.iscelsius



    def __init__(self,fdata,cfg:OpenWeatherMapSettings):
    
        self.iscelsius = cfg.IsCelsius 
    
        self.t =  datetime.datetime.fromtimestamp(int(fdata['dt']))
        self.id = int(fdata['weather'][0]['id'])

        if ('clouds' in fdata) and ('all' in fdata['clouds']):
            self.clouds = int(fdata['clouds']['all'])
        else:
            self.clouds = 0
        
        if ('rain' in fdata) :
            if ('3h' in fdata['rain']):
                self.rain = float(fdata['rain']['3h'])
            elif ('2h' in fdata['rain']):
                self.rain = float(fdata['rain']['2h']) #todo: limit range
            elif ('1h' in fdata['rain']):
                self.rain = float(fdata['rain']['1h']) #todo: limit range
        else:
            self.rain = 0.0

        if ('snow' in fdata):
            if ('3h' in fdata['snow']):
                self.snow = float(fdata['snow']['3h'])
            elif ('2h' in fdata['snow']):
                self.snow = float(fdata['snow']['2h']) #todo: limit range
            elif ('1h' in fdata['snow']):
                self.snow = float(fdata['snow']['1h']) #todo: limit range
        else:
            self.snow = 0.0

        if ('wind' in fdata) and ('speed' in fdata['wind']):
            self.windspeed = float(fdata['wind']['speed'])
        else:
            self.windspeed = 0.0

        if ('wind' in fdata) and ('deg' in fdata['wind']):
            self.winddeg = float(fdata['wind']['deg'])
        else:
            self.winddeg = 0.0

        self.temp = self.toCelsius( float(fdata['main']['temp']) )
        self.temp_fahrenheit = self.toFahrenheit( float(fdata['main']['temp']) )

        self.pressure = float(fdata['main']['pressure'])


    def Print(self):
        print("%s %i %03i%%  %.2f %.2f  %+.2f (%5.1f,%03i)"  % (str(self.t),self.id,self.clouds,self.rain,self.snow,self.temp,self.windspeed,self.winddeg)  )

    @staticmethod
    def Check(fdata):
        if not ('dt' in fdata):
            return False
        if not ('weather' in fdata):
            return False
        if not ('main' in fdata):
            return False
        return True




        
class OpenWeatherMap():
        

    OWMURL = "http://api.openweathermap.org/data/2.5/"


    FILENAME_CURR = "openweathermap_curr_"
    FILENAME_FORECAST = "openweathermap_fcst_"
    FILENAME_EXT = ".json"
    
    FILETOOOLD_SEC = 15*60 # 15 mins
    TOOMUCHTIME_SEC = 4*60*60 # 4 hours 


    def __init__(self,cfg:OpenWeatherMapSettings):
        assert cfg!=None
        assert cfg.OWM_LAT!=None
        assert cfg.OWM_LON!=None
        assert cfg.OWM_KEY!=None
        
        self.cfg = cfg
        reqstr = "lat=%.4f&lon=%.4f&mode=json&APPID=%s" % (self.LAT,self.LON,self.cfg.OWM_KEY)
        self.URL_FOREAST = self.OWMURL+"forecast?"+reqstr
        self.URL_CURR =  self.OWMURL+"weather?"+reqstr
        self.f = []
        
        if not os.path.exists(self.cfg.rootdir):
            os.makedirs(self.cfg.rootdir)

        self.filename_forecast = os.path.join(self.cfg.rootdir,self.FILENAME_FORECAST+self.PLACEKEY+self.FILENAME_EXT)
        self.filename_curr = os.path.join(self.cfg.rootdir,self.FILENAME_CURR+self.PLACEKEY+self.FILENAME_EXT)

    @property
    def LAT(self)->float:
        return self.cfg.OWM_LAT

    @property
    def LON(self)->float:
        return self.cfg.OWM_LON
    
    @staticmethod
    def MakeCoordinateKey(p:float):
        n=int(p*10000)
        return ( "%08X"  % ( n if n>=0 else (n+(1 << 32)) ))[2:]
            
    @property    
    def PLACEKEY(self)->str:
        return  OpenWeatherMap.MakePlaceKey(self.LAT,self.LON)
    
    @staticmethod    
    def MakePlaceKey(latitude:float,longitude:float):
        return  OpenWeatherMap.MakeCoordinateKey(latitude) + OpenWeatherMap.MakeCoordinateKey(longitude)

    def FromWWW(self):
    
        fjsontext = urlopen(self.URL_FOREAST).read()
        fdata = json.loads(fjsontext)
        ff = open(self.filename_forecast,"wb")
        ff.write( json.dumps(fdata, indent=4).encode('utf-8',errors='ignore') )
        ff.close()
        
        cjsontext = urlopen(self.URL_CURR).read()
        cdata = json.loads(cjsontext)
        cf = open(self.filename_curr,"wb")
        cf.write( json.dumps(cdata, indent=4).encode('utf-8',errors='ignore') )
        cf.close()
        
        return self.FromJSON(cdata,fdata)





    def GetTempRange(self,maxtime):
        if len(self.f)==0:
            return None
        tmax = -999
        tmin = 999
        isfirst = True
        for f in self.f:
            if (isfirst):
                isfirst = False
                continue
            if (f.t>maxtime):
                break
            if (f.temp>tmax):
                tmax = f.temp
            if (f.temp<tmin):
                tmin = f.temp
        return (tmin,tmax)


    def FromJSON(self,data_curr,data_fcst):
        self.f = []
        cdata = data_curr
        f = WeatherInfo(cdata,self.cfg)
        self.f.append(f)
        if not ('list' in data_fcst):
            return False
        for fdata in data_fcst['list']:
            if not WeatherInfo.Check(fdata):
                continue
            f = WeatherInfo(fdata,self.cfg)
            self.f.append(f)
        return True



    def FromFile(self):
        ff = open(self.filename_forecast)
        fdata = json.load(ff)
        ff.close()
        cf = open(self.filename_curr)
        cdata = json.load(cf)
        cf.close()
        
        return self.FromJSON(cdata,fdata)

    def IsFileTooOld(self, filename):
        return (not os.path.isfile(filename)) or ( (time.time() - os.stat(filename).st_mtime) > self.FILETOOOLD_SEC )

    def FromAuto(self):
        if (self.IsFileTooOld(self.filename_forecast) or self.IsFileTooOld(self.filename_curr)):
            print("Using WWW")
            return self.FromWWW()
       
        print("Using Cache '%s','%s'" % (self.filename_curr,self.filename_forecast))
        return self.FromFile()

    def GetCurr(self):
        if len(self.f)==0:
            return None
        return self.f[0]


    def Get(self,time):
        for f in self.f:
            if (f.t>time):
                return f
        return None



    def PrintAll(self):
        for f in self.f:
            f.Print()

       




