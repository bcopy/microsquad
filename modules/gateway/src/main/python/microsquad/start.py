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
    print("Queuing " + msg.topic+" "+str(msg.payload.decode('ascii')))
    queue.append(msg)



radio.config(length=200, channel=12, group=12)
radio.on()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

queue = []

client.connect("localhost", 1883, 60)

client.loop_start()

while True:
    inmsg = radio.receive()
    if inmsg != "None":
        print(inmsg)
    if len(queue) > 0:
        outmsg = queue.pop(0)
        print("Sending " + outmsg.topic+" "+str(outmsg.payload.decode('ascii')) +" (left "+str(len(queue))+")")
        radio.send(str(outmsg.payload.decode('ascii')))
    sleep(10)