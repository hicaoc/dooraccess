import utime
import _thread
import config
from machine import UART
import function

class Pn532: 
    def __init__(self):
        self.uart = UART(2, baudrate=115200, rx=config.pn532rx,tx=config.pn532tx,timeout=10)   
        self.wake = bytearray([0x55, 0x55, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,0xff, 0x03, 0xfd, 0xd4, 0x14, 0x01, 0x17, 0x00])
        #self.querycard = bytearray([0x00, 0x00, 0xFF, 0x04, 0xFC, 0xD4, 0x4A, 0x02, 0x00, 0xE0, 0x00])
        self.getid = bytearray([0x00, 0x00, 0xFF, 0x04, 0xFC, 0xD4, 0x4A, 0x01, 0x00, 0xE1, 0x00])
      
        self.uart.write(self.wake)
        function.openspeaker()
        print('init pn532 ok ,',self.uart.read())
        
  
    def getuid(self):
      #utime.sleep_ms(100)
     # print(' '.join(['{:02X}'.format(i) for i in self.getid]))
      self.uart.write(self.getid)
      utime.sleep_ms(10)
    
      if self.uart.any():
          bin_data = self.uart.read()
          #print(' '.join(['{:02X}'.format(i) for i in bin_data]) )   
          
 
         # if len(bin_data) >= 25 and bin_data[0:6]==bytearray([0x00,0x00,0xff,0x00,0xff,0x00]): 
                    
 #           data = ''.join(['{:02X}'.format(i) for i in bin_data[25:29]])
         #   data = ''.join(['{:02X}'.format(i) for i in bin_data[19:23]])          
         #   _thread.start_new_thread(function.openLED,())
         #   return data
            
          if bin_data[0:6] == bytearray([0x00,0x00,0xff,0x0c,0xf4,0xd5]) or bin_data[0:6] == bytearray([0x00,0x00,0xff,0x11,0xef,0xd5]):
            data = ''.join(['{:02X}'.format(i) for i in bin_data[13:17]])
            _thread.start_new_thread(function.openLED,()) 
            return data
          
      return None

def testpn532():  
  p=Pn532()
  while True:
   
    print("uid:",p.getuid())
    utime.sleep_ms(3000)
    
#testpn532()




