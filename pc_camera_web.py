from flask import Flask, render_template, Response
import numpy as np
import cv2
import time

app = Flask(__name__)

cap = cv2.VideoCapture(0)
# # Test with Gstreamer-enabled OpenCV python library
# # Works with sample udp video stream send to 8002 port --> gst-launch-1.0 -v videotestsrc ! video/x-raw,framerate=20/1 ! videoscale ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay ! udpsink port=8002
# cap = cv2.VideoCapture('udpsrc port=8002 caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! rtph264depay ! decodebin ! videoconvert ! appsink', cv2.CAP_GSTREAMER)

def gen_frames():  # generate frame by frame from camera
    counter = 0
    while True:
        # Capture frame-by-frame
        # counter = counter + 1
        success, frame = cap.read()  # read the camera frame
        # if success and counter==10:
        #     counter = 0
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
    app.run(debug=True, port=5001)