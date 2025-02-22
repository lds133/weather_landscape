
from p_weather.sprites import Sprites
from p_weather.openweathermap import OpenWeatherMap,WeatherInfo
from p_weather.sunrise import sun

import datetime 
from PIL import Image
import random


class DrawWeather():

    XSTART = 32
    XSTEP  = 44
    XFLAT =  10

    YSTEP = 50  #64
    
    DEFAULT_DEGREE_PER_PIXEL = 0.5

    
    FLOWER_RIGHT_PX = 15
    FLOWER_LEFT_PX = 10
    
    
    @staticmethod
    def mybeizelfnc(t,d0,d1,d2,d3):
        return  (1-t)*( (1-t)*((1-t)*d0+t*d1 ) + t*( (1-t)*d1 + t*d2)) + t*( (1-t)*( (1-t)*d1 + t*d2)+t*((1-t)*d2 +t*d3))


    def mybezier(self,x,xa,ya,xb,yb):
        xc = (xb+xa)/2.0
        d = xb-xa
        t = float(x-xa)/float(d)
        y = DrawWeather.mybeizelfnc(t,ya,ya,yb,yb)
        return int(y)
        #print(t,x,y)




    def __init__(self,canvas,sprites):

        self.img = canvas
        self.sprite = sprites
        (self.IMGEWIDTH,self.IMGHEIGHT) = self.img.size


    def TimeDiffToPixels(self,dt):
       ds = dt.total_seconds() 
       secondsperpixel = (WeatherInfo.FORECAST_PERIOD_HOURS*60*60) / DrawWeather.XSTEP
       return int ( ds / secondsperpixel )


    def DegToPix(self,t):
        n = (t - self.tmin)/self.degreeperpixel
        y = self.ypos+self.YSTEP - int(n)
        return y



    def BlockRange(self,tline,x0,x1):
        for x in range(x0,x1):
            tline[x] = Sprites.DISABLED
            


    def DrawTemperature(self,f:WeatherInfo,x:int,y:int):
        if (f.IsCelsius):
            self.sprite.DrawInt(f.PrintableTemperature,x,y+10,True,2)
        else:
            self.sprite.DrawInt(f.PrintableTemperature,x,y+10,False,1)




    #todo: add thunderstorm
    #todo: add fog
    def Draw(self,ypos:int,owm:OpenWeatherMap):


        self.picheight = self.IMGHEIGHT
        self.picwidth = self.IMGEWIDTH
        self.ypos = ypos

        nforecasrt = ( (self.picwidth-self.XSTART)/self.XSTEP ) 
        maxtime = datetime.datetime.now() + datetime.timedelta(hours=WeatherInfo.FORECAST_PERIOD_HOURS*nforecasrt)

        (self.tmin,self.tmax) = owm.GetTempRange(maxtime)
        self.temprange = self.tmax-self.tmin
        if ( self.temprange < self.YSTEP ):
            self.degreeperpixel = self.DEFAULT_DEGREE_PER_PIXEL
        else:
            self.degreeperpixel = self.temprange/float(self.YSTEP)
        
        #print("tmin = %f , tmax = %f, range=%f" % (self.tmin,self.tmax,self.temprange))

        xpos=0
        tline = [0]*(self.picwidth+self.XSTEP*2)
        f = owm.GetCurr()
        oldtemp = f.temp
        oldy = self.DegToPix(oldtemp)
        for i in range(self.XSTART):
            tline[i] = oldy
        yclouds = int(ypos-self.YSTEP/2)
        f.Print()

        self.sprite.Draw("house",0,xpos,oldy) 
        
       
        # convert pressure to smoke angle 
        curr_hpa = owm.GetCurr().pressure
        smokeangle_deg = ((curr_hpa - owm.cfg.PRESSURE_MIN) / (owm.cfg.PRESSURE_MAX-owm.cfg.PRESSURE_MIN) )*85 + 5
        if (smokeangle_deg<0):
            smokeangle_deg=0
        if (smokeangle_deg>90):
            smokeangle_deg=90
        self.sprite.DrawSmoke(xpos+21,self.picheight-oldy+23,smokeangle_deg)
        
        self.DrawTemperature(f,xpos+8,oldy)
        self.sprite.DrawCloud(f.clouds,xpos,yclouds,self.XSTART,self.YSTEP/2)
        self.sprite.DrawRain(f.rain,xpos,yclouds,self.XSTART,tline)
        self.sprite.DrawSnow(f.snow,xpos,yclouds,self.XSTART,tline)


        t = datetime.datetime.now()#+datetime.timedelta(hours = 1, minutes=0)
        
        
        dt = datetime.timedelta(hours=WeatherInfo.FORECAST_PERIOD_HOURS)
        tf = t 
        
        x0 = int(self.XSTART)
        xpos = x0
        nforecasrt = int(nforecasrt)

        n = int( (self.XSTEP-self.XFLAT)/2 )
        for i in range(nforecasrt+1):
            f = owm.Get(tf)
            if (f==None):
                continue
                
            #f.Print()
            
            newtemp = f.temp
            newy = self.DegToPix(newtemp)
            
            for i in range(n):
                tline[xpos+i] = self.mybezier(xpos+i,xpos,oldy,xpos+n,newy)

            for i in range(self.XFLAT):
                tline[int(xpos+i+n)] = newy

            xpos+=n+self.XFLAT

            n = (self.XSTEP-self.XFLAT)
            oldtemp = newtemp
            oldy = newy
            tf += dt

        
        tline0 = tline.copy()
        
        self.BlockRange(tline,0,x0)
        
        
        s=sun(owm.LAT,owm.LON) 
        tf = t 
        xpos = self.XSTART
        objcounter=0
        for i in range(nforecasrt+1):
            f = owm.Get(tf)
            if (f==None):
                continue

            t_sunrise = s.sunrise(tf)
            t_sunset = s.sunset(tf) 
            t_noon = datetime.datetime(tf.year,tf.month,tf.day,12,0,0,0)
            t_midn = datetime.datetime(tf.year,tf.month,tf.day,0,0,0,0)+datetime.timedelta(days=1)
            
           #print(tf," - ",tf + dt,"   ",t_noon,t_midn)

            ymoon = ypos-self.YSTEP*5/8

            if (tf<=t_sunrise) and (tf+dt>t_sunrise):
                dx = self.TimeDiffToPixels(t_sunrise-tf)  - self.XSTEP/2
                self.sprite.Draw("sun",0,xpos+dx,ymoon)
                objcounter+=1
                if (objcounter==2):
                    break;

            if (tf<=t_sunset) and (tf+dt>t_sunset):
                dx = self.TimeDiffToPixels(t_sunset-tf)  - self.XSTEP/2
                self.sprite.Draw("moon",0,xpos+dx,ymoon)
                objcounter+=1
                if (objcounter==2):
                    break;
                    
            if (tf<=t_noon) and (tf+dt>t_noon):
                dx = self.TimeDiffToPixels(t_noon-tf)  - self.XSTEP/2
                ix =int(xpos+dx)
                self.sprite.Draw("flower",1,ix,tline[ix]+1)
                self.BlockRange(tline,ix-self.FLOWER_LEFT_PX,ix+self.FLOWER_RIGHT_PX)


            if (tf<=t_midn) and (tf+dt>t_midn):
                dx = self.TimeDiffToPixels(t_midn-tf)  - self.XSTEP/2
                ix =int(xpos+dx)
                self.sprite.Draw("flower",0,ix,tline[ix]+1)      
                self.BlockRange(tline,ix-self.FLOWER_LEFT_PX,ix+self.FLOWER_RIGHT_PX)
                    

            xpos+=self.XSTEP
            tf += dt
        

 
        istminprinted = False
        istmaxprinted = False
        tf = t 
        xpos = self.XSTART
        n = int( (self.XSTEP-self.XFLAT)/2 )
        f_used = []
        
        for i in range(nforecasrt+1):
            f = owm.Get(tf)
            if (f==None):
                continue
 
            f.Print()
            dx = self.TimeDiffToPixels(f.t-tf)  - self.XSTEP/2
            ix =int(xpos+dx)
            
            yclouds = int( ypos-self.YSTEP/2 )
            
            if (f.temp==self.tmin) and (not istminprinted):
                self.DrawTemperature(f,xpos+n,tline0[xpos+n])
                istminprinted = True
            
            if (f.temp==self.tmax) and (not istmaxprinted):
                self.DrawTemperature(f,xpos+n,tline0[xpos+n])
                istmaxprinted = True


            # todo: apply sprite line width 
            if not (f in f_used):
                self.sprite.DrawWind(f.windspeed,f.winddeg,ix,tline)
                self.sprite.DrawCloud(f.clouds,ix,yclouds,self.XSTEP,self.YSTEP/2)
                self.sprite.DrawRain(f.rain,ix,yclouds,self.XSTEP,tline0)
                self.sprite.DrawSnow(f.snow,ix,yclouds,self.XSTEP,tline0)
                f_used.append(f)
                
            

            xpos+=self.XSTEP
            tf += dt




        BLACK = 0

        for x in range(self.picwidth):
            if (tline0[x]<self.picheight):
                self.sprite.Dot(x,tline0[x],Sprites.BLACK)
            else:
                print("out of range: %i - %i(max %i)" % (x,tline0[x],self.picheight))




