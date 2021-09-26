#FROM debian:stable-slim
#FROM ubuntu:impish
FROM python:slim-buster

USER root

RUN apt update
RUN apt -y upgrade
RUN pip3 install configparser
RUN pip3 install flask
RUN pip3 install schedule

# copy files
COPY containerstart.sh /app/containerstart.sh
COPY clickdelay.py /app/clickdelay.py
COPY clickdelay.ini /app/clickdelay.ini
COPY html /app/html
COPY timer1.py /app/timer1.py
COPY timer1.ini /app/timer1.ini

# set workdir
WORKDIR /app

# run the command on container startup
CMD ["./containerstart.sh"]
