# Human Detection examples

A set of simple Python scripts for accessing camera video feed (pc camera / rtsp video feed) via OpenCV & simple Human Detection scenarios.

The best script is the Tensorflow based example in the `tf_example` folder.

Libraries used:
- flask (for web based app)
- opencv-python (pip)
- tensorflow
- numpy

## Dockerized Human Detection service with web access

### Build the service

After cloning the project, go to the `docker` directory and run:

```bash
$ docker build -t human_detection .
```

in order to build the service. 

**Exposed ports: 5000 (for web access).**

For building the same dockerized service with enabled Gstreamer backend support, run:

```bash
$ docker build -t human_detection_gst -f ./Dockerfile-gst .
```

**Exposed ports: 5001 (for web access), 8002 (for receiving UDP video stream).**

### Run the service

Start the container with this command:

```bash
$ docker run --rm -it --net=host --entrypoint "/bin/bash" human_detection
```

or:

```bash
$ docker run --rm -it --net=host --entrypoint "/bin/bash" human_detection_gst
```

depending on the service you wish to run.

Inside the container, navigate to the `./human_detection/tf_example` directory, edit the `RCNN_inception_v2_human_detection_rtsp_web.py` with the correct RTSP link and, lastly run:

```bash
$ python3 RCNN_inception_v2_human_detection_rtsp_web.py
```

The same scripts can be used for obtaining video feed with Gstreamer backend, by editing the `cap = cv2.VideoCapture()` line with the correct Gstreamer pipeline. A sample pipeline can be found in the `pc_camera_web.py` script.

You can then access the web service via this URL: `http://localhost:5000` or `http://localhost:5000/video_feed` .