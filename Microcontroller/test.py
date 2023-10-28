import threading

t1=10
t=None
def hello():
    global t1;
    print(t1)
    t1-=1
    t = threading.Timer(1, hello)
    t.start()
    if(t1==0):
        t.cancel()

hello()
