
import machine
from machine import Pin,I2C
import ssd1306
from time import sleep
import framebuf
import ds1302
import web
import _thread

ds = ds1302.DS1302(Pin(5),Pin(18),Pin(19))#设置时钟接口
i2c = I2C(scl=Pin(21), sda=Pin(22), freq=400000) #设置通讯参数
oled = ssd1306.SSD1306_I2C(128,64, i2c) #定义屏幕参数

oled.poweron()
oled.init_display()

def wifi_thread():#定义开启WiFi连接线程
    web.start_connect()
    
    
def oled_thread():
    while True:
        oled.fill(0)
        oled.chinese("请连接",1,1)
        oled.text(":TESTWIFI",50,4)
        oled.chinese("访问",1,4)
        oled.text(":192.168.4.1",33,28)
        time_list=ds.date_time()
        time_view = "{}:{}:{}".format(time_list[4],time_list[5],time_list[6])
        day_view = "{}.{}.{} {}".format(time_list[0],time_list[1],time_list[2],time_list[3])
        oled.text(time_view,41,44)
        oled.text(day_view,24,56)
        oled.show()
        
def power_on():#开机设置参数
    oled.fill(0)
    oled.chinese("欢迎使用",3,4)
    oled.show()    
    sleep(1)
    _thread.start_new_thread(wifi_thread, ())
    _thread.start_new_thread(oled_thread, ())


       

power_on()
