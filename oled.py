from machine import Pin,I2C
import ssd1306
import utime
import config
import fonts
import function


i2c = I2C(scl=Pin(config.oledSCL), sda=Pin(config.oledSDA), freq=100000)
lcd=ssd1306.SSD1306_I2C(128,64,i2c)


def chinese(ch_str, x_axis, y_axis): 
   offset_ = 0 
   y_axis = y_axis*8  # 中文高度一行占8个  
   x_axis = (x_axis*16)  # 中文宽度占16个 
   for k in ch_str: 
       code = 0x00  # 将中文转成16进制编码 
       data_code = k.encode("utf-8") 
       code |= data_code[0] << 16 
       code |= data_code[1] << 8
       code |= data_code[2]
       #print(data_code)
       byte_data = fonts.fonts.get(code)
       if byte_data==None:
         print(code)
         continue
       for y in range(0, 16):
           a_ = bin(byte_data[y]).replace('0b', '')
           while len(a_) < 8:
               a_ = '0'+a_
           b_ = bin(byte_data[y+16]).replace('0b', '')
           while len(b_) < 8:
               b_ = '0'+b_
           for x in range(0, 8):
               lcd.pixel(x_axis+offset_+x, y+y_axis, int(a_[x]))   
               lcd.pixel(x_axis+offset_+x+8, y+y_axis, int(b_[x]))   
       offset_ += 16


def showlcd(name):
    try:
        while True:
            lcd.text("www.greatbit.com",0,0)
            tm = function.timestr()
            datastr=tm[0:4]+'.'+tm[4:6]+'.'+tm[6:8]
            timestr=tm[8:10]+':'+tm[10:12]+':'+tm[12:14]
            chinese(name[0],2,2)
            lcd.text(name[1],32,36) 
            lcd.text(timestr,32,46)
            lcd.text(datastr,24,56)
            lcd.show()      #display pix
            utime.sleep_ms(10)
            lcd.fill(0)
    except OSError:
        print('oled error')     

#name=['曹程','12344567']
#showlcd(name)



