import sys
import socketio
import eventlet
import json
import time
import math
from flask import Flask, render_template
import socket
from threading import Thread

admins=[]
connected = []

def web_hello(env, start_response):
    # connected.append(ws)
    print(f"[WS] Client connected")
    start_response('200 OK', [('Content-Type', 'text/json')])
    return "Test 1"
    """
    try:
        while True:
            from_browser = ws.wait()
            print(from_browser)
            if(from_browser is None):
                break
            ws.send(json.dumps({
                 'zone_1': 1,
                 'zone_2': 1,
                 'zone_3': 1
                 }))
            print('[WS] ', from_browser)
    except:
        the_type, the_value, the_traceback = sys.exc_info()
        print(the_type, the_value, the_traceback);
    finally:
        print(f"[WS] Client disconnected")
        return connected.remove(ws)
    """

app = Flask(__name__, static_folder='static')

sio = socketio.Server(cors_allowed_origins=[
    "https://h211wj9ekda-496ff2e9c6d22116-0-colab.googleusercontent.com",
    "https://amritb.github.io",
    "https://admin.socket.io",
    "http://localhost:3000",
    "https://4aa4-2409-40e2-1c-b3bf-4dd3-2abc-1664-c5da.ngrok-free.app",
    "http://192.168.88.107:3000",
    "http://192.168.43.245:3000"
    ],
    async_mode='threading'
                      )
sio.instrument(auth={
    'username': 'admin',
    'password': "admin123",
})

app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

@sio.event
def connect(sid, environ):
    all_sockets = []
    for nsp in sio.manager.get_namespaces():
        for sid, eio_sid in sio.manager.get_participants(
            nsp, None):
                all_sockets.append(sid)

    print('[Socket.IO] Client connected:', sid)
    sio.emit('response_info/clients', data={'clients': all_sockets})

@sio.event
def disconnect(sid1):
    all_sockets = []
    for nsp in sio.manager.get_namespaces():
        for sid, eio_sid in sio.manager.get_participants(
            nsp, None):
                all_sockets.append(sid)
    all_sockets.remove(sid1)
    print('[Socket.IO] Client disconnected:', sid1)
    sio.emit('response_info/clients', data={'clients': all_sockets})

    if(sid1 in admins):
        print("[Socket.IO] Admin disconnected")
        return admins.remove(sid1)

@sio.event
def hello(sid, args):
    print(args, type(json.loads(args)))
@sio.on('request_info/clients') # type: ignore
def request_clients(sid, data):
    all_sockets = []
    for nsp in sio.manager.get_namespaces():
        for sid, eio_sid in sio.manager.get_participants(
            nsp, None):
                all_sockets.append(sid)
    return sio.emit('response_info/clients', data={'clients': all_sockets}, to=sid)

@sio.on('request_access/admin') # type: ignore
def elevate(sid, data):
    if len(admins) == 1: 
        return sio.emit('response_access/admin', data={'status': False}, to=sid)
    if data['username'] == 'admin' and data['password'] == 'admin123':
        admins.append(sid)
        print(admins)
        return sio.emit('response_access/admin', data={'status': True}, to=sid)
    else:
        return sio.emit('response_access/admin', data={'status': False}, to=sid)
    

current_zone=1
timer=-1
t1=None
t2=None
inference_data=None

def updateTime():
    global timer, t1, current_zone;
    print("[Socket.IO] Timer:", timer)
    timer-=1
    if(timer-2<=5 and timer-2>-1):
         update_lights("", {
            "zone": (1 if current_zone==3 else (current_zone+1)%4),
            "color": "yellow",
            "auto": True,
            "time": timer
        })

def setTime(data):
    global current_zone, inferece_data, timer;
    amb= data['ambulance_zones']
    if(len(amb) >0):
        global temp
        temp=[]
        for zone in amb:
            if(data[f"zone_{zone}"] !=0): temp.append(data[f"zone_{zone}"])
        current_zone = int(list(data.keys())[list(data.values()).index(min(temp))][-1]);
        print("[Debug] Current Zone" + str(current_zone))
              
    timer = math.ceil(((5*data["zone_" + str(current_zone)]))/3)
    if(timer==0): timer=0
    elif(timer<5): timer=5
    elif(timer>60): timer=60;
    if(timer!=0):
         timer+=2
         update_lights("", {
            "zone": current_zone,
            "color": "green",
            "auto": True,
            "time": timer
        })
    while timer > -1:
        if(timer==0): current_zone=1 if current_zone==3 else (current_zone+1)%4
        time.sleep(1)
        updateTime()
    setTime(inference_data)

@sio.on('inference') # type: ignore
def inference(sid, data):
    global thread, inference_data;
    inference_data=data
    if(timer<0): 
        thread = Thread(name="detection",target=setTime, args=(inference_data,))
        thread.daemon = True
        thread.start()
    print("[Socket.IO] Inference:", timer)
    return sio.emit('inference', data=data, to=admins[0])

@sio.on('update_lights/update') # type: ignore
def update_lights(sid, data):
    print(data)
    print("[Socket.IO] Connected:", connected)
    if(len(connected) > 0):
        zone, color = data['zone'], data['color']
        print("[Debug WS] ", zone, color)
        new_data = {
             "z": zone,
             "c": 1 if color=="red" else (2 if color=="yellow" else 3),
             "u": True if ("auto" in data.keys()) else False,
             "t": data['time'] if ("time" in data.keys()) else False
        }
        for ws in connected:
            ws.send(f"{json.dumps(new_data)}".encode())
        sio.emit("update_lights/broadcast", new_data)
    return;

@app.route("/")
def index():
    all_sockets = []
    for nsp in sio.manager.get_namespaces():
        for sid, eio_sid in sio.manager.get_participants(
            nsp, None):
                all_sockets.append(sid)
    return render_template("index.html", connected=all_sockets, admins=len(admins))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 4000))
server.listen(5)  # max backlog of connections

print('Listening on {}:{}'.format("0.0.0.0", 4000))


def handle_client_connection(client_socket):
     print("hi")

if __name__ == '__main__':
    t= Thread(name="WS_server", target=app.run, args=('0.0.0.0', 3000,))
    t.start()

    while True:
        client_sock, address = server.accept()
        connected.append(client_sock);
        print('Accepted connection from {}:{}'.format(address[0], address[1]))
        client_handler = Thread(
            target=handle_client_connection,
            args=(client_sock,)  # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
        )
        client_handler.start()