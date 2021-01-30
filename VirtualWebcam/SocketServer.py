import eventlet
import socketio
import VirtualWebcam
import subprocess as sp
from queue import Queue
from threading import Thread

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

message_queue = Queue()
thread = None

@sio.event
def connect(sid, environ):
    if thread == None:
        thread = Thread(target=long_running, args = (message_queue))
        thread.start()
    # # ok
    # pipe = sp.Popen( 'python ./VirtualWebcam.py', shell=True, stdout=sp.PIPE, stderr=sp.PIPE )
    # # res = tuple (stdout, stderr)
    # res = pipe.communicate()
    # print("retcode =", pipe.returncode)
    # print("res =", res)
    # print("stderr =", res[1])
    # for line in res[0].decode(encoding='utf-8').split('\n'):
    # print(line)

    print('connect ', sid)

@sio.event
def setting_change(sid, data):
    print('Setting changed ', data)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)


def long_running(message_queue):
    t = VirtualWebcam(checkSleep=True)
    t.start(message_queue)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)    