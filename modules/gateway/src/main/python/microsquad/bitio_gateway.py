from microbit import display,radio, sleep

import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("uSquad Gateway Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("homie/usquad/gateway/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload.decode('ascii')))
    radio.send(str(msg.payload.decode('ascii')))



radio.config(length=200, channel=12, group=1)
radio.on()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# client.connect("broker.hivemq.com", 1883, 60)
client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_start()

while True:
    msg = radio.receive()
    if msg != "None":
        print(msg)
    sleep(100)