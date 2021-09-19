#FROM debian:stable-slim
#FROM ubuntu:impish
FROM python:slim-buster

USER root

#RUN apt update
#RUN apt -y upgrade
#RUN apt -y install python3 python3-pip
RUN pip3 install configparser
RUN pip3 install flask

# copy files
COPY clickdelay.py /app/clickdelay.py
COPY clickdelay.ini /app/clickdelay.ini
COPY html /app/html

# set workdir
WORKDIR /app

# run the command on container startup
CMD ["python3", "clickdelay.py"]
