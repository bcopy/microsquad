
import logging
import paho.mqtt.client as mqtt_client
import asyncio
import threading
import functools

logger = logging.getLogger(__name__)


class HomieController():
    def __init__(self,mqtt_settings,homie_settings) -> None:
        self.mqtt_settings = mqtt_settings
        self.mqtt_client = None
        self.mqtt_transport = "tcp"
        self.mqtt_protocol = mqtt_client.MQTTv311

    def connect(self):
        logger.debug(
            "MQTT Connecting to {} as client {}".format(
                self.mqtt_settings["MQTT_BROKER"], self.mqtt_settings["MQTT_CLIENT_ID"]
            )
        )
        
        if self.mqtt_settings["MQTT_PROTOCOL"]: 
            if(self.mqtt_settings["MQTT_PROTOCOL"] in [mqtt_client.MQTTv31, mqtt_client.MQTTv311, mqtt_client.MQTTv5]):
                self.mqtt_protocol = self.mqtt_settings["MQTT_PROTOCOL"]
            else:
                logger.info("MQTT protocol {} unsupported ".format(self.mqtt_settings["MQTT_PROTOCOL"]))

        if self.mqtt_settings["MQTT_TRANSPORT"]:  
            self.mqtt_transport = self.mqtt_settings["MQTT_TRANSPORT"]
    
        if self.mqtt_settings["MQTT_WS_PATH"]:  
            self.mqtt_transport = "websockets"

        self.mqtt_client = mqtt_client.Client(client_id=self.mqtt_settings["MQTT_CLIENT_ID"], transport=self.mqtt_transport, protocol=self.mqtt_protocol)
        self.mqtt_connected = False 
        self.mqtt_client.on_connect = self._on_connect
        self.mqtt_client.on_message = self._on_message
        self.mqtt_client.on_disconnect = self._on_disconnect
        
        if self.mqtt_settings["MQTT_USERNAME"]:
            self.mqtt_client.username_pw_set(
                self.mqtt_settings["MQTT_USERNAME"],
                password=self.mqtt_settings["MQTT_PASSWORD"],
            )

        if self.mqtt_settings["MQTT_WS_PATH"]:  
            self.mqtt_client.ws_set_options(path=self.mqtt_settings["MQTT_WS_PATH"])

        if self.mqtt_settings["MQTT_USE_TLS"]:
            self.mqtt_client.tls_set()

        try:
            self.mqtt_client.connect(
                self.mqtt_settings["MQTT_BROKER"],
                port=self.mqtt_settings["MQTT_PORT"],
                keepalive=self.mqtt_settings["MQTT_KEEPALIVE"],
            )
            self.mqtt_client.loop_start()
        except Exception as e:
            logger.warning("Homie Controller MQTT client unable to connect to Broker {}".format(e))


        def start():
            try:
                asyncio.set_event_loop(self.event_loop)
                logger.info ('Starting Homie Controller asyincio publish loop forever')
                self.event_loop.run_forever()
                logger.warning ('Homie Controller Event publish loop stopped')
            except Exception as e:
                logger.error ('Error in Homie Controller event loop {}'.format(e))

        self.event_loop = asyncio.new_event_loop()

        logger.info("Starting Homie Controller MQTT publish thread")
        self._ws_thread = threading.Thread(target=start, args=())

        self._ws_thread.daemon = True
        self._ws_thread.start()

    def publish(self, topic, payload, retain, qos):
        logger.debug(
            "MQTT publish topic: {}, payload: {}, retain {}, qos {}".format(
                topic, payload, retain, qos
            )
        )
        def publish():
            self.mqtt_client.publish(topic, payload, retain=retain, qos=qos)

        self.event_loop.call_soon_threadsafe(functools.partial(publish))

    def _on_connect(self, client, userdata, flags, rc):
        if rc > 0: 
            rc_text = mqtt_client.connack_string(rc)
            logger.fatal("Homie Controller MQTT - connection: Result code {} {}, Flags {}".format(rc, rc_text,flags))
        else:
            logger.debug("Homie Controller MQTT - connection successful : Result code {}, Flags {}".format(rc, flags))


        # TODO : Subscribe to device / node / property patterns under given Homie prefix

        #
        ###########

        self.mqtt_connected = rc == 0

    def _on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode("utf-8")

        # Split the topic into device / node / property

        # Invoke matching handlers
        # * on_new_terminal  (known terminal ?)
        # * on_new_player (known player ?)
        # * on_new_game (known game ?)
        # * on_update_terminal_property (validate terminal name and node ?)


    def _on_disconnect(self, client, userdata, rc):
        self.mqtt_connected = False 
        if rc > 0: 
            rc_text = mqtt_client.error_string(rc)

            logger.warning(
                "Homie Controller MQTT - unexpected disconnection  {} {} Result Code : {} {}".format(client, userdata, rc, rc_text)
            )