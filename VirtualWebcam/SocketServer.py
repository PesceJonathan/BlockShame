import eventlet
from eventlet import wsgi, websocket

import socketio
from VirtualWebcam import VirtualWebcam
import subprocess as sp
from queue import Queue
from threading import Thread
import traceback

sio = socketio.Server()
app = socketio.WSGIApp(sio)

message_queue = Queue()
thread = None

@sio.event
def connect(sid, environ):
    try:
        global thread
        global message_queue
        if thread == None:
            thread = Thread(target=long_running, args = (message_queue,))
            thread.start()
        print('connect ', sid)
    except:
        traceback.print_exc()

@sio.event
def setting_change(sid, data):        
    if data.get("webcam"):
        print('Setting changed', data.get("webcam"))
    elif data.get("accessibility"):
        print('Setting changed', data.get("accessibility"))
    else:
        pass
    # Add the data to Queue
    return "OK", 123

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

print("ASDASDSD")
def long_running(message_queue):
    t = VirtualWebcam(checkSleep=True)
    print("Starting up webcam")
    t.start(message_queue)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)    