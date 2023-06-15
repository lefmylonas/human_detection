
FROM ubuntu:latest

RUN apt update && apt install -y vim git pip libgl1 libglib2.0-0 

RUN pip install tensorflow opencv-python flask

WORKDIR /home/ubuntu

RUN git clone https://github.com/lefmylonas/human_detection.git

EXPOSE 5000