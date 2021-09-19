from threading import Lock
from flask import Flask, render_template, session, request, \
    copy_current_request_context
from flask_socketio import SocketIO, emit, disconnect
import base64
import numpy
import random
from analyzer import *

async_mode = None

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode=async_mode)
thread = None
thread_lock = Lock()

pose_wc = None
pose_vid = None

last_time = 0
last_perf_check = 0
perf = {'dist': 0, 'weight': 0}


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


def calculate_performance():
    global perf
    while True:
        socketio.sleep(2)
        calc_perf(perf)
        socketio.emit('performance',
                      {'value': random.randint(0, 3)})


@socketio.event
def new_frame(frame):
    if not frame:
        return
    jpg_original = base64.b64decode(frame[22:])
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)
    analyze_webcam(img, pose_wc)


@socketio.event
def my_event(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.event
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()
    session['receive_count'] = session.get('receive_count', 0) + 1
    pose_wc.close()
    pose_vid.close()
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)


@socketio.event
def my_ping():
    emit('my_ping')


@socketio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(calculate_performance)

    # Initialize pose ML
    global pose_wc, pose_vid
    pose_wc = mp_pose.Pose(**MP_SETTINGS)
    pose_vid = mp_pose.Pose(**MP_SETTINGS)

    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app)
