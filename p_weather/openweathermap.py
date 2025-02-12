import os
import time
import json
import datetime
from urllib.request import urlopen




class WeatherInfo():

    KTOC = 273.15

    Thunderstorm = 2
    Drizzle = 3
    Rain =5
    Snow=6
    Atmosphere=7
    Clouds =8

    FORECAST_PERIOD_HOURS = 3


    def __init__(self,fdata):
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


        self.temp = float(fdata['main']['temp']) - WeatherInfo.KTOC
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

    def __init__(self,apikey:str,latitude:float,longitude:float,rootdir:str=""):

        self.latitude = latitude
        self.longitude = longitude

        reqstr = "lat=%.4f&lon=%.4f&mode=json&APPID=%s" % (self.LAT,self.LON,apikey)
        self.URL_FOREAST = self.OWMURL+"forecast?"+reqstr
        self.URL_CURR =  self.OWMURL+"weather?"+reqstr
        self.f = []
        self.rootdir = rootdir
        
        if not os.path.exists(self.rootdir):
            os.makedirs(self.rootdir)

        self.filename_forecast = os.path.join(self.rootdir,self.FILENAME_FORECAST+self.PLACEKEY+self.FILENAME_EXT)
        self.filename_curr = os.path.join(self.rootdir,self.FILENAME_CURR+self.PLACEKEY+self.FILENAME_EXT)

    @property
    def LAT(self)->float:
        return self.latitude

    @property
    def LON(self)->float:
        return self.longitude
    
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
        f = WeatherInfo(cdata)
        self.f.append(f)
        if not ('list' in data_fcst):
            return False
        for fdata in data_fcst['list']:
            if not WeatherInfo.Check(fdata):
                continue
            f = WeatherInfo(fdata)
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

       




