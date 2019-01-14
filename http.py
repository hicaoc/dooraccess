import config
import utime
import socket
import network
import machine
import function

sta_if = network.WLAN(network.STA_IF); sta_if.active(True)
sta_if.connect(config.ssid, config.password) # Connect to an AP


while(sta_if.isconnected() == False):
  utime.sleep(1)
ip = sta_if.ifconfig()[0]


function.openspeaker()

while True:
  try:
    function.synctime()
    print(utime.localtime())
    break
  except OSError:
    print('ntp error')     
  utime.sleep(1)
  


addr2 = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s2 = socket.socket()
s2.bind(addr2)
s2.listen(2)


lasttime = utime.time()

def web_page():
  
  if function.door.value() == 1:
    gpio_state="开"
  else:
    gpio_state="关"
  
   # filename = 
  html = """<html><head> <title>南京信风门禁系统</title> 
  <meta charset="UTF-8" name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="data:,"> 
<style>

html{font-family: Helvetica;
display:inline-block;
margin: 0px auto;
text-align: center;
}

h1{color: #0F3376;
padding: 2vh;}
p{font-size: 1.5rem;}

.button{display: inline-block;
background-color: #e7bd3b;
border: none; 
border-radius: 4px;
color: white;
padding: 16px 40px;
text-decoration: none;
font-size: 30px;
margin: 2px;
cursor: pointer;
}

.button2{background-color: #4286f4;}
.button3{background-color: #01DF01;}
</style>
</head><body>

<h1>信风公司门禁</h1> 
<p>门当前状态： <strong>""" + gpio_state + """</strong></p>
<p><a href="/?door=on"><button class="button">开门</button></a></p>
<p><a href="/?door=off"><button class="button button2">关门</button></a></p>
<p><a href="/?download"><button class="button button3">下载</button></a></p>
</body></html>"""
  return html


def accept():

 
  while True:
  #  try:
      conn,addr = s2.accept()
      print('Got a connection from %s' % str(addr))
      request = conn.recv(1024)
      
      #aaa = request.split(b" ")
      
     # print(aaa)
     
      (method, url, version) = request.split(b" ",2)
    
      if b"?" in url:
          (path, query) = url.split(b"?", 2)
      else:
          (path, query) = (url, "")
    
      if query == b"door=on" :
        function.door.value(1)
        global lasttime       
        lasttime = utime.time()
      elif query == b"download":
        pass
        
      else:
        function.door.value(0)
        
      response = web_page()
      conn.send(response)
  #  except:
     #   print("web server error")
      #  conn.write("HTTP/1.1 500 Internal Server Error\r\n\r\n")
      #  conn.write("<h1>Internal Server Error</h1>")
      conn.close()
      







