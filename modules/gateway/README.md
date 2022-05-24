# How to initialize the environment 

```
python3 -m venv usquad-venv
echo "`pwd`/src/main/python `pwd`/src/test/python" > usquad-venv/lib/python3.8/site-packages/gateway.pth
```

# How to use

* Ensure that your MQTT broker is running on port 1883

* Execute:
```
. ./setup-venv.sh
python -m microsquad.gateway.mqtt
```

* Follow the instructions given by Bitio to detect your Micro:bit and the gateway should start.

# How to reset your broker's persistent data (Mosquitto)

```bash
sudo service mosquitto stop
sudo rm /var/lib/mosquitto/mosquitto.db
sudo service mosquitto start
```