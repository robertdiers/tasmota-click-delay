# tasmota-click-delay
website to turn on Tasmota and give delay for automatic turn off - used to trigger circulation and heating pump

### Defaults
please check properties in clickdelay.ini file, could be overridden by Docker env variables

### Docker usage

environment variables:

MQTT_BROKER (default: 192.168.1.7)

MQTT_PORT (default: 1883)

MQTT_USER (default: admin)

MQTT_PASSWORD (default: password)

CIRCULATION_MQTT_NAME (default: tasmota_zirkulation)

HEATINGSYSTEM_MQTT_NAME (default: tasmota_heizungspumpe)

HEATINGSYSTEMTEMP_MQTT_NAME (default: tasmota_bad)

docker run -d --restart always -p 50000:50000 -e MQTT_BROKER=192.168.1.7 -e MQTT_PASSWORD=password --name tasmotaclickdelay ghcr.io/robertdiers/tasmota-click-delay:1.1

### Website: ###

http://localhost:50000/zirkulation

http://localhost:50000/badheizung

### Blog

https://robertdiers.medium.com/sonoff-basic-with-tasmota-auto-off-after-a-time-delay-ca72160e7862
