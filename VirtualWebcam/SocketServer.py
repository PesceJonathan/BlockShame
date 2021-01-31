import eventlet
from eventlet import wsgi, websocket

import socketio
from VirtualWebcam import VirtualWebcam
import subprocess as sp
from queue import Queue
from threading import Thread, Lock
import traceback

sio = socketio.Server()
app = socketio.WSGIApp(sio)

message_queue = Queue()
thread = None
lock = Lock()


@sio.event
def connect(sid, environ):
    print("-------------------CONNECT ", sid)
    try:
        global thread
        global message_queue
        if thread == None:
            thread = Thread(target=long_running, args=(message_queue,))
            thread.start()
        return "OK", 123
    except:
        traceback.print_exc()


@sio.event
def setting_change(sid, data):
    print(data)
    if data.get("webcam"):
        print("Setting changed", data.get("webcam"))
        message_queue.put({"type": "webcam", "payload": data.get("webcam")})
    elif data.get("accessibility"):
        print("Setting changed", data.get("accessibility"))
        message_queue.put(
            {"type": "accessibility", "payload": data.get("accessibility")}
        )
    elif data.get("audio"):
        print("Setting changed", data.get("audio"))
        message_queue.put({"type": "audio", "payload": data.get("audio")})
    else:
        pass
    # Add the data to Queue
    return "OK", 123


@sio.event
def disconnect(sid):
    print("disconnect ", sid)


print("ASDASDSD")


def long_running(message_queue):
    t = VirtualWebcam(lock)
    print("Starting up webcam")
    t.start(message_queue)


if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(("", 5000)), app)
