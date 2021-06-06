import paho.mqtt.client as mqtt

import logging

# ##################################
# MicroSquad Gateway MQTT implementation

class MqttGateway:
    def __init__(self, connector):
        self.client = mqtt.Client()
        self.client.on_connect = self.__on_connect
        self.client.on_message = self.__on_message
        self.dispatching = False
        self.connector = connector

    # The callback for when the client receives a CONNACK response from the server.
    def __on_connect(self,client, userdata, flags, rc):
        logging.info("uSquad Gateway Connected with result code "+str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        self.client.subscribe("homie/usquad/gateway/#")

    # The callback for when a PUBLISH message is received from the server.
    def __on_message(self, client, userdata, msg):
        logging.info("Queuing " + msg.topic+" "+str(msg.payload.decode('ascii')))
        self.queue.append(msg)

    def init(self):
        self.client.connect("localhost", 1883, 60)

    def start(self):
        self.dispatching = True
        self.client.loop_start()
        self.connector.start()

 