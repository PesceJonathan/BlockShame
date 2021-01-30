import eventlet
import socketio
import VirtualWebcam
import subprocess as sp
from threading import Thread
sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

@sio.event
def connect(sid, environ):

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

def Webcam_process
if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)    