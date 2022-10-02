FROM docker.io/debian:stable-slim

RUN apt update
RUN apt -y upgrade
RUN apt -y install cron python3 python3-pip

RUN pip3 install configparser flask paho-mqtt

# copy files
COPY clickdelay.py /app/clickdelay.py
COPY stopcirculation.py /app/stopcirculation.py
COPY clickdelay.ini /app/clickdelay.ini
RUN chmod 777 /app/clickdelay.ini
COPY TasmotaCirculation.py /app/TasmotaCirculation.py
COPY html /app/html

COPY entrypoint.sh /app/entrypoint.sh
COPY container_cron /etc/cron.d/container_cron

# set workdir
WORKDIR /app

# give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/container_cron

# apply cron job
RUN crontab /etc/cron.d/container_cron

# run the command on container startup
CMD ["bash", "entrypoint.sh"]