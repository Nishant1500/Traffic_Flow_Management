from machine import Pin
from dotenv import dotenv_values as env
import time
import usocket as socket
import tm1637
import network
import ujson as json
import _thread

ENV = env("config.env")

led = Pin(5, Pin.OUT)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ENV["SSID"], ENV["PASS"])
display = tm1637.TM1637(clk=Pin(16), dio=Pin(17))

# Wait for connect or fail
max_wait = 20
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    display.scroll("Error")
    time.sleep(2)
    display.scroll(str(wlan.status()))
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip: ' + status[0] )
    display.scroll('ip' + f"{status[0]}".replace(".", "-"))

print(wlan.ifconfig())

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.88.107", 4000))

led_config = [
    [[5,4,3],[1,0,0],[0,1,0],[0,0,1]],
    [[6,7,8],[1,0,0],[0,1,0],[0,0,1]],
    [[9,11,10],[1,0,0],[0,1,0],[0,0,1]]
]

def socket_thread():
    while True:
        data = s.recv(1024)
        if data:
            print(data.decode())
            try:
                d = json.loads(data.decode())
                updateTimer(d)
                updateZone(d['z'], d['c'])
                if(d['u'] == True):
                    updateZone(1 if d['z']==3 else (d['z']+1)%4, 1)
                    updateZone(3 if d['z']==1 else (d['z']+3)%4, 1)
            except:
                # do something'
                print("Error");

timer= -1
def updateTimer(data):
    global timer;

    if(timer<=-1 or timer==False):
        timer = data['t'] - 2

def updateZone(z, c):
    global led_config;
    z-=1
    leds= []

    for pin_no in led_config[z][0]:
        leds.append(Pin(pin_no, Pin.OUT))

    for n in range(3):
        leds[n].value(led_config[z][c][n])

_thread.start_new_thread(socket_thread, ())
zerDisplayed = False

while True:
    print(f"Timer: {timer}")
    if(timer > -1):
        display.number(timer)
        timer-=1
        time.sleep(1)
    else:
        if(not zerDisplayed):
            display.number(0)
            zerDisplayed = True
        else:
            display.show("    ")
            zerDisplayed = False
        time.sleep(0.5)