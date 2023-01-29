# tasmota-click-delay
website to turn on Tasmota and give delay for automatic turn off - used to trigger circulation pump

### Defaults
plaese check properties in clickdelay.ini file, could be overridden by Docker env variables

### Docker usage

environment variables:

CIRCULATION_MQTT_BROKER (default: 192.168.1.7)

CIRCULATION_MQTT_PORT (default: 1883)

CIRCULATION_MQTT_USER (default: admin)

CIRCULATION_MQTT_PASSWORD (default: password)

CIRCULATION_MQTT_NAME (default: tasmota_zirkulation)

docker run -d --restart always -p 50000:50000 -e CIRCULATION_MQTT_PASSWORD=password --name tasmotaclickdelay ghcr.io/robertdiers/tasmota-click-delay:1.0

### Website: ###
http://localhost:50000/zirkulation

### Blog
https://robertdiers.medium.com/sonoff-basic-with-tasmota-auto-off-after-a-time-delay-ca72160e7862
