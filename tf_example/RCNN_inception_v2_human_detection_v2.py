# import the necessary packages
import numpy as np
import cv2
from persondetection import DetectorAPI
import time
 
cv2.startWindowThread()

# open webcam video stream
cap = cv2.VideoCapture(0)
odapi = DetectorAPI()
threshold = 0.7

# prev_frame_time = 0
# new_frame_time = 0

while(True):
    # Calculate fps of camera by grabbing a few frames
    num_frames = 10;
    start = time.time()
    for i in range(0, num_frames) :
        ret, frame = cap.read()
    end = time.time()
    fps  = num_frames / (end - start)
    fps = int(fps)
    fps = str(fps)

    img = cv2.resize(frame, (800, 600))
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
    
    cv2.putText(img, 'Status : Detecting ', (40,40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
    cv2.putText(img, f'Total Persons : {person}', (40,70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
    cv2.putText(img, f'fps : {fps}', (40,100), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
    
# Display the resulting frame
    cv2.imshow('frame',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
# finally, close the window
cv2.destroyAllWindows()
cv2.waitKey(1)