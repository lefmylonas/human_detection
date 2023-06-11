# Python script based on the solution proposed in the link below:
# https://stackoverflow.com/questions/49233433/opencv-read-errorh264-0x8f915e0-error-while-decoding-mb-53-20-bytestream

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

def Receive():
    global cap
    cap = cv2.VideoCapture('rtsp://username:password@@ip:port/Streaming/Channels/101', cv2.CAP_FFMPEG)
    ret, frame = cap.read()
    q.put(frame)
    while ret:
        ret, frame = cap.read()
        q.put(frame)


def Display():
    cv2.startWindowThread()
    odapi = DetectorAPI()
    threshold = 0.7
    while True:
        if q.empty() !=True:          
           frame=q.get()
           img = cv2.resize(frame, (1280, 720), interpolation = cv2.INTER_AREA)
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
            
           cv2.putText(img, 'Status : Detecting ', (40,100), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
           cv2.putText(img, f'Total Persons : {person}', (40,130), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
           # cv2.putText(img, f'fps : {fps}', (40,160), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)

           # Display the resulting frame
           cv2.imshow('frame',img)
           if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    # When everything done, release the capture
    global cap
    cap.release()
    # finally, close the window
    cv2.destroyAllWindows()
    cv2.waitKey(1)
            
if __name__=='__main__':
    p1=threading.Thread(target=Receive)
    p2 = threading.Thread(target=Display)
    p1.start()
    p2.start()