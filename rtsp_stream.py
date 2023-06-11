#!/usr/bin/env python3.6

import cv2
 
RTSP_URL = 'rtsp://username:password@@ip:port/Streaming/Channels/101' # depends on camera
 
cap = cv2.VideoCapture(RTSP_URL)
 
if not cap.isOpened():
    print('Cannot open RTSP stream')
    exit(-1)
 
while True:
    ret, frame = cap.read()

    width = 1280
    height = 720
    dim = (width, height)
    img = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
    
    cv2.imshow('RTSP stream', img)
 
    if cv2.waitKey(1) == 27:
        break
 
cap.release()
cv2.destroyAllWindows()
