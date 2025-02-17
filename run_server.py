
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
           

        if (self.path.startswith('/'+EINKFILENAME)) or (self.path.startswith('/'+USERFILENAME)):
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
       
        if not self.IsFileTooOld(user_file_name):
            return
       
        img = WEATHER.MakeImage() 
        img.save(user_file_name) 
        
        img = img.rotate(-90, expand=True)   
        img = img.transpose(Image.FLIP_TOP_BOTTOM)  
        
        img.save(eink_file_name) 
        
        
        
        


    def IndexHtml(self):
    
        body = '<h1>Weather as Landscape</h1>'
        body+='<p>Place: '+("%.4f" % secrets.OWM_LAT) +' , '+("%.4f" % secrets.OWM_LON)+'</p>'
        body+='<p><img src="'+USERFILENAME+'" alt="Weather" "></p>'
        body+='<p>ESP32 URL: <span id="eink"></span></p>'
        body+='<script> document.getElementById("eink").innerHTML = window.location+"'+EINKFILENAME+'" ;</script>'
            
            
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


