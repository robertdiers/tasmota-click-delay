FROM python:slim-buster

USER root

RUN apt update
RUN apt -y upgrade
RUN pip3 install configparser flask paho-mqtt

# copy files
COPY clickdelay.py /app/clickdelay.py
RUN chmod u+x /app/clickdelay.py
COPY clickdelay.ini /app/clickdelay.ini
COPY TasmotaCirculation.py /app/TasmotaCirculation.py
COPY html /app/html

# set workdir
WORKDIR /app

# run the command on container startup
CMD ["python3", "clickdelay.py"]
