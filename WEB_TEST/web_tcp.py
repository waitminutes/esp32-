
'''此程序为服务器端程序，主要功能是开启热点，当有设备连接后，建立接口开始监听，同时调用客户端程序，实现收发消息'''
import network
import socket
import ure
import time
import web_main
# import ds1302
from machine import Pin
import _thread
import dhtx
import machine



view = web_main.web_viewer
lock = _thread.allocate_lock()


class web_demo():
    def __init__(self,switch_state="初始化",test_number=0,
                ON_number=0,OFF_number=0,response = view.config_page(),
                TEM=None,HUM=None,cont=0 ,light = machine.ADC(machine.Pin(33))):
        self.switch_state = switch_state
        self.ON_number = ON_number
        self.OFF_number = OFF_number
        self.response = response
        self.test_number = test_number
        self.TEM = TEM
        self.HUM = HUM
        self.cont = cont
        self.light = light
        self.light.atten(machine.ADC.ATTN_11DB)
    def startsocket(self):#，定义一个套接字，开启监听

        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('0.0.0.0', 80))
        self.server_socket.listen(10)
        self.start_work()#启动主操作
        
    def start_work(self):#等待客户端连接热点
        try:
            while True: 
                self.conn, self.addr = self.server_socket.accept()#创建套接字阻塞，当有人浏览器输入ip时往下执行
               #for i in range(3):# 每当accetp()一个新的conn，另开3个子线程来处理任务
                _thread.start_new_thread(self.recv_thread, ())#开启接受信息的线程，主线程创建一个套接字等待其他客户端请求
                time.sleep(0.015)
        except:
            print("出错")

            time.sleep(0.015)
            
    def recv_thread(self):
        while True:
            
            try:
                #self.conn.settimeout(3)
                request = b""
  
                request = self.conn.recv(512)#接受数据
              
                
                if  request is not None:
                   
                    try:#对接受到的数据进行正则匹配
                        url = ure.search("(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP", request).group(1).decode("utf-8").rstrip("/")
                    except:
                        print("无响应")
                        pass
                    print("url is: ",url)
                    if url == "":#当客户端只是在浏览器输入了ip，则返回一个空白的url
                        self.conn.sendall('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
                        self.conn.sendall(self.response)#发送主页面程序
                        
                    elif url == "temperature_numberer":
                        self.temperature()
                        
                    elif url == "humidity_numberer":
                        self.humidity()
                    elif url == "light_intensity":
                        self.light_intensity()                        
                    elif url == "LED_ON":
                        self.LED_STATE("LED_ON")
                        print("led开")
                    elif url == "LED_OFF":
                        self.LED_STATE("LED_OFF")
                        print("led关")
                        
                    else:
                        pass
                else:      
                    break
                    #self.start_work()
                     #发送数据
            finally:
                self.conn.close()         
            _thread.exit()



    def temperature(self):#向客户端发送温度数据
        content1 = "{}".format(self.TEM)
        try:
            self.conn.sendall(content1)
            print("温度:{}".format(self.TEM))
        except:
           pass
        

    def humidity(self):#向客户端发送湿度数据
        content1 = "{}".format(self.HUM)
        try:
            self.conn.sendall(content1)
            print("湿度:{}".format(self.HUM))
        except:
            pass
    def light_intensity(self):#光照强度函数，可编辑
        content1 = "{}".format(self.light.read())
        try:
            self.conn.sendall(content1)
            print("光照强度:{}".format(self.light.read()))
        except:
            pass
        
    def LED_STATE(self,led_code):#向客户端发送LED状态
        if led_code == "LED_ON":
            self.switch_state="LED_ON"
#             machine.Pin(15,machine.Pin.OUT).value(1)
            content1 = "{}".format(self.switch_state)
            try:
                self.conn.sendall(content1)

                print("灯已开")
            except:
               pass
        else:
            self.switch_state="LED_OFF"
            content1 = "{}".format(self.switch_state)
            try:
                self.conn.sendall(content1)
                print("灯已关")
            except:
               pass                

    def timekeeping_thread(self):
        while True:
            self.cont += 1
            self.TEM = dhtx.get_dht_temperature('dht11',32)
            self.HUM = dhtx.get_dht_relative_humidity('dht11',32)
            time.sleep(1)
            print(self.TEM,self.HUM,"已运行：{}次".format(self.cont))


if __name__=='__main__':
    web = web_demo()#实例化类11
    _thread.start_new_thread(web.timekeeping_thread, ())
    web.startsocket()#开启热点
    while True:
        pass
    
    



