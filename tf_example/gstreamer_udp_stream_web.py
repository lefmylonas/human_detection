# Python script based on the solution proposed in the link below:
# https://stackoverflow.com/questions/49233433/opencv-read-errorh264-0x8f915e0-error-while-decoding-mb-53-20-bytestream

from flask import Flask, render_template, Response
import numpy as np
import cv2
from persondetection import DetectorAPI
# import time
import queue
import threading
q=queue.Queue()
# import os
# os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

    # prev_frame_time = 0
    # new_frame_time = 0

    # # Calculate fps of camera by grabbing a few frames
    # num_frames = 10;
    # start = time.time()
    # for i in range(0, num_frames) :
    #     ret, frame = cap.read()
    # end = time.time()
    # fps  = num_frames / (end - start)
    # fps = int(fps)
    # fps = str(fps)

app = Flask(__name__)
odapi = DetectorAPI()
threshold = 0.7    

def Receive():
    global cap
    counter = 0
    cap = cv2.VideoCapture('udpsrc port=8002 buffer-size=2097152 ! application/x-rtp, media=video, encoding-name=H264 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! videoflip method=rotate-180 ! appsink', cv2.CAP_GSTREAMER)
    ret, frame = cap.read()
    q.put(frame)
    while ret:
        # counter = counter + 1
        ret, frame = cap.read()
        # reduce frames to be driven to the human detection app
        # if counter==10:
        q.put(frame)
            # counter = 0


def Display():
    while True:
        if q.empty() !=True:          
           img=q.get()
        #    img = cv2.resize(frame, (1280, 720), interpolation = cv2.INTER_AREA)
           boxes, scores, classes, num = odapi.processFrame(img)
           person = 0
           acc = 0
           for i in range(len(boxes)): 
                if classes[i] == 1 and scores[i] > threshold:
                    box = boxes[i]
                    person += 1
                    cv2.rectangle(img, (box[1], box[0]), (box[3], box[2]), (255, 0, 0), 2)  # cv2.FILLED
                    cv2.putText(img, f'P{person, round(scores[i], 2)}', (box[1] - 30, box[0] - 8),cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)  # (75,0,130),

           # # Calculate processed video fps
           # new_frame_time = time.time()
           # fps = 1/(new_frame_time-prev_frame_time)
           # prev_frame_time = new_frame_time
           # fps = int(fps)
           # fps = str(fps)
            
           cv2.putText(img, 'Status : Detecting ', (50,200), cv2.FONT_HERSHEY_DUPLEX, 1.8, (255,0,0), 3)
           cv2.putText(img, f'Total Persons : {person}', (50,260), cv2.FONT_HERSHEY_DUPLEX, 1.8, (255,0,0), 3)
           # cv2.putText(img, f'fps : {fps}', (40,160), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)

           ret, buffer = cv2.imencode('.jpg', img)
           frame = buffer.tobytes()
           yield (b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
            

@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(Display(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

if __name__=='__main__':
    p1=threading.Thread(target=Receive)
    p2 = threading.Thread(target=Display)
    p1.start()
    p2.start()
    app.run(host='0.0.0.0', port=5001)
    # app.run(debug=True)
