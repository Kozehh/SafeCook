# USAGE
# python main.py -w <adresse_ip_serveur_debug> -o <weight_file> -c <cfg_file> -n <classes_name_file> 
# -i <information_processing_service_ip>

import time
import argparse
import cv2
import base64
from Image_processing import Yolo
from Protocole import *


class obj_detection_client(object):
    def __init__(self, server_addr, stream_fps):
        self.server_addr = server_addr
        self.server_port = 5001
        self.stream_fps = stream_fps
        self.last_update_t = time.time()
        self.wait_t = (1/self.stream_fps)

    def setup(self, client):
        print('[INFO] Connecting to server http://{}:{}...'.format(
			self.server_addr, self.server_port))
        client.sio.connect(
			'http://{}:{}'.format(self.server_addr, self.server_port),
			transports=['websocket'],
			namespaces=['/video_feed'])
        time.sleep(1)
        return self

    def image_to_jpeg(self, image):
        # Encode frame as jpeg
        frame = cv2.imencode('.jpg', image)[1].tobytes()
        # Encode frame in base64 representation and remove
        # utf-8 encoding
        frame = base64.b64encode(frame).decode('utf-8')
        return "data:image/jpeg;base64,{}".format(frame)

    def send_data(self, frame, text, client):
        curr_t = time.time()
        if curr_t - self.last_update_t > self.wait_t:
            self.last_update_t = curr_t
            client.sio.emit(
				'objdetserver',
				{
					'image': self.image_to_jpeg(frame),
     				'text': '<br />'.join(text)
				}
			)

    def check_exit(self):
        pass

    def close(self, client):
        client.sio.disconnect()


def main(server_addr, stream_fps, objDetector, sioClient, zmqReciever, socketClient):

    # Load the model and classes
    objDetector.load()
    streamer = None
    try:
        # Init client object
        streamer = obj_detection_client(server_addr, stream_fps).setup(sioClient)

        # start looping over all the frames
        while True:
            # receive RPi name and frame from the RPi and acknowledge
            # the receipt
            (rpiName, frame) = zmqReciever.receive_frame()
            text = ["Objects"]
            # Process the frame recieved
            frame, data, text = objDetector.processImage(frame, text)

            # Send and recieve data to information processing service
            socketClient.send_msg(data)
            socketClient.receive_msg()
            
            # Send to web debugging interface all the objects detected in the frame
            streamer.send_data(frame, text, sioClient)

            if streamer.check_exit():
                break
            
    finally:
        if streamer is not None:
            streamer.close(sioClient)
   
if __name__ == "__main__":
    # Args
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-w", "--web_addr", required=True,
        help="the web server ip address that streams the frames captured")
    ap.add_argument("-o", "--obj_weights", required=True,
        help="the name of the weights file")
    ap.add_argument("-c", "--obj_cfg", required=True,
        help="the name of the cfg file")
    ap.add_argument("-n", "--obj_names", required=True,
        help="the name of the names file")
    ap.add_argument("-i", "--service_address", required=True,
        help="the service address")
    args = vars(ap.parse_args())


    # Connexion et initialization des protocoles
    # Get a socketIO client
    sioClient = SioClient()
    # Create a zmq reciever
    zmqReciever = Zmq()
    # Initialise YOLO object with the model
    objDetector = Yolo(args["obj_weights"], args["obj_cfg"], args["obj_names"])
    # Initialise zmq socket to communicate with information processing service
    socketClient = Socket(args["service_address"])
    socketClient.init()
    
    main(args["web_addr"], 30, objDetector, sioClient, zmqReciever, socketClient)
    
