import imagezmq
import zmq
import socketio

class Socket:
    def __init__(self, web_addr):
        self.web_addr = web_addr
        self.socket = None

    def init(self):
        # Attempt connection to server
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect(self.web_addr)

    def receive_msg(self):
        return self.socket.recv()

    def send_msg(self, msg):
        return self.socket.send_string(str(msg))


class Zmq:
    def __init__(self):
        # initialize the ImageHub object
        self.imageHub = imagezmq.ImageHub()        

    def receive_frame(self):
        (rpiName, frame) = self.imageHub.recv_image()
        self.imageHub.send_reply(b'OK')
        return rpiName, frame
        
class SioClient:
    sio = socketio.Client()
    def __init__(self):
        sio = socketio.Client()
        
    @sio.event
    def connect():
        print('[INFO] Sucessfully connected to server.')
            
    @sio.event
    def disconnect():
        print('[INFO] Disconnected from server.')
        
    @sio.event
    def connect_error():
        print('[INFO] Failed to connect to server.')
        
    