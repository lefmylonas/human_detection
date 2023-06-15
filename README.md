# Human Detection examples

A set of simple Python scripts for accessing camera video feed (pc camera / rtsp video feed) via OpenCV & simple Human Detection scenarios.

The best script is the Tensorflow based example in the `tf_example` folder.

Libraries used:
- flask (for web based app)
- opencv-python (pip)
- tensorflow
- numpy

## Dockerized Human Detection service with web access

After cloning the project, go to the `docker` directory and run:

```bash
$ docker build -t human_detection .
```

in order to build the service.

After this, start the container with this command:

```bash
$ docker run --rm -it --net=host --entrypoint "/bin/bash" human_detection
```

Inside the container, navigate to the `./human_detection/tf_example` directory, edit the `RCNN_inception_v2_human_detection_rtsp_web.py` with the correct RTSP link and, lastly run:

```bash
$ python3 RCNN_inception_v2_human_detection_rtsp_web.py
```

You can then access the web service via this URL: `http://localhost:5000/video_feed` .