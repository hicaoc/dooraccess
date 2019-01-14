import utime
import _thread
import config
import function

import oled
name=['请刷卡','12345678']
_thread.start_new_thread(oled.showlcd,(name,))

import http
_thread.start_new_thread(http.accept,())


print('http and lcd init ok!')

lasttime = utime.time()
lastmonth = function.timestr()[0:6]

file = open('uid.txt','rt')
UidMap = {}
datas = file.read()
for line in datas.split("\r"):
  lineSplit = line.split(",")
  if len(lineSplit) >= 2:
    UidMap[lineSplit[0]] = lineSplit[1]
 
logfile = open('uidlog.'+function.timestr()[0:6]+'.txt','a+')

import pn532
p532 = pn532.Pn532()

function.openspeaker()


import socket
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) 


while True:
    #print("+++",utime.localtime())
  
    utime.sleep_ms(300) 
  
    if function.timestr()[0:6] !=  lastmonth :      
      logfile.close()
      logfile = open('uidlog.'+function.timestr()[0:6]+'.txt','a+')
      
      try:
        function.synctime()
        print(utime.localtime())
      except OSError:
        print('ntp error')   
  
    if utime.time()-lasttime > config.doorOpenTimeout:
      function.door.value(0)
      name[0] = '请刷卡'
      name[1]='--------' 
 
    uid = p532.getuid()
    
    if uid == None :
      continue
    
    tt = function.timestr()
    ss = ''
          
    if (uid in UidMap.keys()):
      function.door.value(1)
      name[0] = UidMap[uid]      
      lasttime = utime.time()
      ss = tt+','+UidMap[uid]+','+uid+',0'
            
    else:
      name[0] = '未登记卡' 
      ss = tt+',未登记卡,'+uid+',1'
      lasttime = utime.time()
      function.openspeaker()
      
    name[1] = uid
    
    s.sendto(ss,(config.dstip,config.dstport))
    logfile.write(ss+'\n') 
    logfile.flush()
    
    #print(ss)
    #print('---',utime.localtime())
    
   

    
          
      
          













