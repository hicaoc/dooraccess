import machine
from machine import Pin
import ustruct as struct
import socket
import config
import utime

led=Pin(config.ledPin,Pin.OUT)        #create LED object from pin2,Set Pin2 to output
door=Pin(config.doorPin,Pin.OUT)

p25=machine.Pin(config.speakerPin)
speaker=machine.PWM(p25)
speaker.duty(0)
speaker.freq(1000)

def openspeaker():
  speaker.duty(100)
  utime.sleep_ms(200)
  speaker.duty(0)
  
def openLED():
  speaker.duty(50)
  led.value(1)            #Set led turn on
  utime.sleep_ms(100)
  speaker.duty(0) 
  led.value(0)
  utime.sleep_ms(50)  
  led.value(1)            #Set led turn on
  utime.sleep_ms(100)  
  led.value(0)#Set led turn off
  
def synctime():
    tm = utime.localtime(getntptime()) 
    tm = tm[0:3] + (0,) + tm[3:6] + (0,)   
    machine.RTC().datetime(tm)
  
def getntptime():
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1b
    addr = socket.getaddrinfo(config.ntpserver, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(3)
    res = s.sendto(NTP_QUERY, addr)
    msg = s.recv(48)
    s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    return val - 3155673600

def timestr():
    tm = utime.localtime()  
    year=str(tm[0])
    mouth="{:0>2d}".format(tm[1])
    day=tm[2]
    hour=tm[3]
    sencod="{:0>2d}".format(tm[5])
    if 16<=hour<24:  #ntp授时获取的是格林尼治时间 这里我们转换为我们东8区的时间
      day=day+1   
    hour=hour+8    
    min="{:0>2d}".format(tm[4])    
    if hour>24:
      hour=hour-24
    hour = "{:0>2d}".format(hour)
    day = "{:0>2d}".format(day)
    return  year+mouth+day+hour+min+sencod    
    
#print(getntptime())






