from flask import Flask, render_template, Response
import numpy as np
import cv2
import time

app = Flask(__name__)

cap = cv2.VideoCapture(0)

def gen_frames():  # generate frame by frame from camera
    counter = 0
    while True:
        # Capture frame-by-frame
        counter = counter + 1
        success, frame = cap.read()  # read the camera frame
        if success and counter==10:
            counter = 0
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)