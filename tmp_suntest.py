import datetime
from p_weather.sunrise import sun


OWM_LAT = 52.196136
OWM_LON = 21.007963

print(OWM_LAT,",",OWM_LON)

s = sun(OWM_LAT,OWM_LON)

year = 2025
month = 5

for day in range(1,30):
    when = datetime.datetime(year,month,day)
    sr = s.sunrise(when)
    ss = s.sunset(when)
    
    print("%04i-%02i-%02i" % (year,month,day)," - ","%02i:%02i" % (sr.hour, sr.minute)," , ","%02i:%02i" % (ss.hour, ss.minute) )