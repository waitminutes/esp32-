import network

def ap():
    wlan_ap = network.WLAN(network.AP_IF)
    wlan_ap.active(True)
    wlan_ap.config(essid='TESTWIFI',authmode=0)#开启热点TESTWIFI
    
if __name__=='__main__':
    ap()