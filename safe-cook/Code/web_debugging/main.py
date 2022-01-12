from flask import request, Flask, render_template
from flask_socketio import SocketIO
import argparse

# initialize a flask object
app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def index():
	"""Home page"""
	return render_template('index.html')
 
@socketio.on('connect', namespace='/web')
def connect_web():
    print('[INFO] Web client connected: {}'.format(request.sid))
    
@socketio.on('disconnect', namespace='/web')
def disconnect_web():
    print('[INFO] Web client disconnected: {}'.format(request.sid))
    
@socketio.on('connect', namespace='/video_feed')
def connect_feed():
    print('[INFO] Object detection client connected: {}'.format(request.sid))


@socketio.on('disconnect', namespace='/video_feed')
def disconnect_feed():
    print('[INFO] Object detection client disconnected: {}'.format(request.sid))


@socketio.on('objdetserver')
def handle_cv_message(message):
    socketio.emit('server2web', message, namespace='/web')
    
# check to see if this is the main thread of execution
if __name__ == '__main__':
	# construct the argument parser and parse command line arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--ip", type=str,
		help="ip address of the device")
	ap.add_argument("-p", "--port", type=int,
		help="port number of the server (1024 to 65535)")
	args = vars(ap.parse_args())

	print('[INFO] Starting server at http://localhost:5001')
	# start the flask app
	socketio.run(app=app, host='0.0.0.0', port=5001)



