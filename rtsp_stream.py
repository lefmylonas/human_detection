import cv2
# import os
# os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
 
RTSP_URL = 'rtsp://username:password@ip:port/Streaming/Channels/101'
 
cv2.startWindowThread()
cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)
 
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
 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # breaking the loop if the user types q
        # note that the video window must be highlighted!
        break
 
cap.release()
cv2.destroyAllWindows()
# the following is necessary on the mac,
# maybe not on other platforms:
cv2.waitKey(1)
