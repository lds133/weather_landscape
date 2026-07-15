
import os
import time
import datetime
from PIL import Image

from http.server import HTTPServer, BaseHTTPRequestHandler

import secrets

import socket

from weather_landscape import WeatherLandscape
from configs import *

SERV_IPADDR = "0.0.0.0"
SERV_PORT = 3355
FAVICON = "favicon.ico"
FILETOOOLD_SEC = 60*10


WEATHERS = [    WeatherLandscape(WLConfig_BW())          ,
                WeatherLandscape(WLConfig_BWI())         ,
                WeatherLandscape(WLConfig_EINK())        ,
                WeatherLandscape(WLConfig_RGB_Black())   ,
                WeatherLandscape(WLConfig_RGB_White())   ,
                # ── Fahrenheit variants ──
                WeatherLandscape(WLConfig_BW_F())        ,
                WeatherLandscape(WLConfig_BWI_F())       ,
                WeatherLandscape(WLConfig_EINK_F())      ,
                WeatherLandscape(WLConfig_RGB_Black_F()) ,
                WeatherLandscape(WLConfig_RGB_White_F()) ,
                ]
                


class WeatherLandscapeServer(BaseHTTPRequestHandler):


    def do_GET_sendfile(self,filepath:str,mimo:str):
        try:
            f = open(filepath, "rb") 
            databytes =  f.read()               
            f.close()  
        except Exception as e:
            databytes = None
            print("File read error '%s' :%s" % (filepath,str(e)))
            
        if (databytes!=None):
            self.send_response(200)
            self.send_header("Content-type", mimo)
        else:
            self.send_response(404)
       
        self.end_headers()
        if (databytes!=None):
            self.wfile.write(databytes)  
    

    def do_GET(self):
        
        if self.path == '/':
           self.path = '/index.html'
           
        print("GET:",self.path)

        if (self.path.startswith('/'+FAVICON)):
            self.do_GET_sendfile(FAVICON,"image/ico")
            return

           
        if (self.path.startswith('/index.html')):
           self.send_response(200)
           self.end_headers()
           self.wfile.write(bytes(self.IndexHtml(), 'utf-8'))
           return
           

        for w in WEATHERS:
            if self.path == '/'+w.cfg.OUT_FILENAME:
                file_name = self.CreateWeatherImage(w) 
                mime = w.cfg.GetMIME()
                assert mime!=None, "Unsuported image file extension"
                self.do_GET_sendfile(file_name ,mime)
                return
            
        print("Path not accessible:",self.path)
        self.send_response(403)
        self.end_headers()



    def IsFileTooOld(self, filename):
        return (not os.path.isfile(filename)) or ( (time.time() - os.stat(filename).st_mtime) > FILETOOOLD_SEC )


    def CreateWeatherImage(self,weather):
        file_name = weather.cfg.ImageFilePath()
        
        if not self.IsFileTooOld(file_name):
            return file_name
       
        return weather.SaveImage()
       
        
        
        


    def IndexHtml(self):
    
   
        body = '<h1>Weather as Landscape</h1>'
        
        for w in WEATHERS:
            id = 'id_'+w.cfg.OUT_FILENAME
            body+='<h2>'+w.cfg.TITLE+'</h2>'  
            #body+='<p>Place: '+("%.4f" % w.cfg.OWM_LAT) +' , '+("%.4f" % w.cfg.OWM_LON)+'</p>'
            body+='<p><img src="'+w.cfg.OUT_FILENAME+'" alt="'+w.cfg.TITLE+'" "></p>'
            body+='<h4>URL: <span id="'+id+'"></span></h4>'
            body+='<script> document.getElementById("'+id+'").innerHTML = window.location+"'+w.cfg.OUT_FILENAME+'" ;</script>'
            body+='<p>&nbsp;</p>'
            
        return """
            <!DOCTYPE html>
            <html lang="en">
              <head>
                <meta charset="utf-8">
                <title>Weather as Landscape</title>
              </head>
              <body> """ + body + """
              </body>
            </html>"""

        
    
#todo: implement support for multiple network interfaces
def get_my_ips():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80)) 
        yield s.getsockname()[0]  
    finally:
        s.close()

    



httpd = HTTPServer((SERV_IPADDR,SERV_PORT),WeatherLandscapeServer)
for ip in get_my_ips():
    print(r"Serving at http://%s:%i/" % (ip,SERV_PORT))
httpd.serve_forever() 




# IPV6
#class HTTPServerV6(HTTPServer):
#    address_family = socket.AF_INET6    
#httpd = HTTPServerV6(('::',SERV_PORT),WeatherLandscapeServer)
#httpd.serve_forever() 