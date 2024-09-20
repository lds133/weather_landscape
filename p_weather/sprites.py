import os
from PIL import Image
import random

class Sprites():

    Black = 0
    White = 1

    BLACK=0
    WHITE=1
    RED  =2
    TRANS=3

    PLASSPRITE = 10
    MINUSSPRITE = 11
    
    EXT = ".png"
    

    def __init__(self,spritesdir,canvas):
        self.img = canvas
        self.pix = self.img.load()
        self.dir = spritesdir
        self.ext = self.EXT
        self.w, self.h = self.img.size



    def Dot(self,x,y,color):
    
        #y = self.h - y
    
        if (y>=self.h) or (x>=self.w) or (y<0) or (x<0):
            return
    
        self.pix[x,y] = color
        

    def Draw(self,name,index,xpos,ypos):

        #print("DRAW '%s' #%i at %i,%i" % (name,index,xpos,ypos))
    
        imagefilename = "%s_%02i%s" % (name, index, self.ext)
        imagepath = os.path.join(self.dir,imagefilename) 
        img = Image.open(imagepath)
        w, h = img.size
        pix = img.load()
        ypos -= h
        for x in range(w):
            for y in range(h):
                if (xpos+x>=self.w) or (xpos+x<0):
                    continue
                if (ypos+y>=self.h) or (ypos+y<0):
                    continue
                if (pix[x,y]==self.BLACK):
                    self.Dot(xpos+x,ypos+y,self.Black)
                elif (pix[x,y]==self.WHITE):
                    self.Dot(xpos+x,ypos+y,self.White)
                elif (pix[x,y]==self.RED):
                    self.Dot(xpos+x,ypos+y,self.Black)

        return w


    DIGITPLAS = 10
    DIGITMINUS = 11
    DIGITSEMICOLON = 12

    def DrawInt(self,n,xpos,ypos,issign=True,isleadzero=False):
        if (n<0):
            sign = self.DIGITMINUS
        else:
            sign = self.DIGITPLAS
        n = round(n)
        n = abs(n)
        n1 = n / 10
        n2 = n % 10
        dx = 0
        if (issign):
            w = self.Draw("digit",sign,xpos+dx,ypos)
            dx+=w+1
        if (n1!=0) or (isleadzero):
            w = self.Draw("digit",n1,xpos+dx,ypos)
            dx+=w+1
        w = self.Draw("digit",n2,xpos+dx,ypos)
        dx+=w+1
        return dx

    def DrawClock(self,xpos,ypos,h,m):
        dx=0
        w = self.DrawInt(h,xpos+dx,ypos,False,True)
        dx+=w
        w = self.Draw("digit",self.DIGITSEMICOLON,xpos+dx,ypos)
        dx+=w
        dx = self.DrawInt(m,xpos+dx,ypos,False,True)
        dx+=w+1
        return dx




    CLOUDWMAX =32
    CLOUDS = [2,3,5,10,30,50]
    CLOUDK = 0.5

    def DrawCloud(self,persent,xpos,ypos,width,height):
        if (persent<2):
            return
        elif (persent<5):
            cloudset = [2]
        elif (persent<10):
            cloudset = [3,2]
        elif (persent<20):
            cloudset = [5,3,2]
        elif (persent<30):
            cloudset = [10,5]
        elif (persent<40):
            cloudset = [10,10]
        elif (persent<50):
            cloudset = [10,10,5]
        elif (persent<60):
            cloudset = [30,5]
        elif (persent<70):
            cloudset = [30,10]
        elif (persent<80):
            cloudset = [30,10,5,5]
        elif (persent<90):
            cloudset = [30,10,10]
        else:
            cloudset = [50,30,10,10,5]

        dx = width 
        dy = 16
        for c in cloudset: 
            self.Draw("cloud",c,xpos+random.randrange(dx),ypos)
        
    HEAVYRAIN = 5.0
    RAINFACTOR = 20

    def DrawRain(self,value,xpos,ypos,width,tline):
        ypos+=1
        r = 1.0 - ( value / self.HEAVYRAIN ) / self.RAINFACTOR 

        for x in range(xpos,xpos+width):
            for y in range(ypos,tline[x],2):
                if (x>=self.w): 
                    continue
                if (y>=self.h): 
                    continue
                if (random.random()>r):
                    self.pix[x,y] = self.Black
                    self.pix[x,y-1] = self.Black
        
    HEAVYSNOW = 5.0
    SNOWFACTOR = 10
    
    def DrawSnow(self,value,xpos,ypos,width,tline):
        ypos+=1
        r = 1.0 - ( value / self.HEAVYSNOW ) / self.SNOWFACTOR 

        for x in range(xpos,xpos+width):
            for y in range(ypos,tline[x],2):
                if (x>=self.w): 
                    continue
                if (y>=self.h): 
                    continue
                if (random.random()>r):
                    self.pix[x,y] = self.Black




    def  DrawWind_degdist(self, deg1,deg2 ):
        h = max(deg1,deg2)
        l = min(deg1,deg2)
        d = h-l
        if (d>180):
            d = 360-d
        return d
    


    def DrawWind_dirsprite(self,dir,dir0,name,list):
        count = [4,3,3,2,2,1,1]
        step = 11.25 #degrees
        dist = self. DrawWind_degdist(dir,dir0)
        n = int(dist/step)
        if (n<len(count)):
            for i in range(0,count[n]):
                list.append(name)
        




    def DrawWind(self,speed,direction,xpos,tline):
            
            list = []

            self.DrawWind_dirsprite(direction,0,  "pine",list)
            self.DrawWind_dirsprite(direction,90, "east",list)
            self.DrawWind_dirsprite(direction,180,"palm",list)
            self.DrawWind_dirsprite(direction,270,"tree",list)

            random.shuffle(list)

            windindex = None
            if   (speed<=0.4):
                windindex = []
            elif (speed<=0.7):
                windindex = [0]
            elif (speed<=1.7):
                windindex = [1,0,0]
            elif (speed<=3.3):
                windindex = [1,1,0,0]
            elif (speed<=5.2):
                windindex = [1,2,0,0]
            elif (speed<=7.4):
                windindex = [1,2,2,0]
            elif (speed<=9.8):
                windindex = [1,2,3,0]
            elif (speed<=12.4):
                windindex = [2,2,3,0]            
            else:
                windindex = [3,3,3,3]    
            
            
            if (windindex!=None):
                ix = int(xpos)
                random.shuffle(windindex)
                j=0
                #print("wind>>>",direction,speed,list,windindex);
                for i in windindex:
                    offset = ix+5
                    if (offset>=len(tline)):
                        break
                    self.Draw(list[j],i,ix,tline[offset]+1) 
                    ix+=9
                    j+=1
                


if __name__ == "__main__":  


    img = Image.open('../test.bmp')
    
    
    s = Sprites('../sprite',img)
    
    
    s.Draw("house",0,100,100)
    
    img.save("../tmp/sprites_test.bmp")
    
    