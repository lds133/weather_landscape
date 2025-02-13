
import os
import time
import datetime
from PIL import Image

from http.server import HTTPServer, BaseHTTPRequestHandler

import secrets

import socket

from weather_landscape import WeatherLandscape


SERV_IPADDR = "0.0.0.0"
SERV_PORT = 3355

EINKFILENAME = "test.bmp"
USERFILENAME = "test1.bmp"
EINKFILENAME_F = "test_f.bmp"
USERFILENAME_F = "test1_f.bmp"
FAVICON = "favicon.ico"

FILETOOOLD_SEC = 60*10

WEATHER = WeatherLandscape()


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
        
        fahrenheit = False
        components = self.path.split('?')
        if len(components) > 1:
            self.path, query = components
            if query == 'fahrenheit=true':
                fahrenheit = True

        if self.path == '/':
           self.path = '/index.html'
           
        print("GET:",self.path)

        if (self.path.startswith('/'+FAVICON)):
            self.do_GET_sendfile(FAVICON,"image/ico")
            return

           
        if (self.path.startswith('/index.html')):
           self.send_response(200)
           self.end_headers()
           self.wfile.write(bytes(self.IndexHtml(fahrenheit), 'utf-8'))
           return
           

        if self.isImageRequest():
            self.CreateWeatherImages()
            file_name = WEATHER.TmpFilePath(self.path[1:])
            self.do_GET_sendfile(file_name ,"image/bmp")
            return
            
        print("Path not accessible:",self.path)
        self.send_response(403)
        self.end_headers()


    def IsFileTooOld(self, filename):
        return (not os.path.isfile(filename)) or ( (time.time() - os.stat(filename).st_mtime) > FILETOOOLD_SEC )


    def CreateWeatherImages(self):
                    
        user_file_name = WEATHER.TmpFilePath(USERFILENAME)
        eink_file_name = WEATHER.TmpFilePath(EINKFILENAME)
        user_file_name_f = WEATHER.TmpFilePath(USERFILENAME_F)
        eink_file_name_f = WEATHER.TmpFilePath(EINKFILENAME_F)
       
        if not self.IsFileTooOld(user_file_name):
            return
       
        # generate Celsius images
        self.generateImages(user_file_name, eink_file_name)

        # generate Fahrenheit images
        self.generateImages(user_file_name_f, eink_file_name_f, True)


    def generateImages(self, user_file_name, eink_file_name, fahrenheit=False):
        img = WEATHER.MakeImage(fahrenheit)
        img.save(user_file_name)
        
        img = img.rotate(-90, expand=True)   
        img = img.transpose(Image.FLIP_TOP_BOTTOM)  
        
        img.save(eink_file_name)


    def isImageRequest(self):
        for filename in [EINKFILENAME, EINKFILENAME_F, USERFILENAME, USERFILENAME_F]:
            if self.path.startswith('/' + filename):
                return True
        return False


    def IndexHtml(self, fahrenheit=False):
        filename = USERFILENAME
        einkfilename = EINKFILENAME
        if fahrenheit:
            filename = USERFILENAME_F
            einkfilename = EINKFILENAME_F
    
        body = '<h1>Weather as Landscape</h1>'
        body+='<p>Place: '+("%.4f" % secrets.OWM_LAT) +' , '+("%.4f" % secrets.OWM_LON)+'</p>'
        body+='<p><img src="'+filename+'" alt="Weather" "></p>'
        body+='<p>ESP32 URL: <span id="eink"></span></p>'
        body+='<script> document.getElementById("eink").innerHTML = window.location.protocol+"//"+window.location.host+window.location.pathname+"'+einkfilename+'" ;</script>'
            
            
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


