service mosquitto stop
rm /var/lib/mosquitto/mosquitto.db
service mosquitto start
service mosquitto status