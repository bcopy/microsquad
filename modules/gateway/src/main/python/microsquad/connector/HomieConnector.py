from line_protocol_parser import parse_line

from homie.device_status import Device_Status
from homie.node.property import property_string

class HomieConnector:

    def __init__(self, homie_root_topic, mqtt_settings):
        self.__homie_root_topic = homie_root_topic

        """ mqtt_settings = {
            'MQTT_BROKER' : 'your.mqtt.server',
            'MQTT_PORT' : 1883,
            'MQTT_SHARE_CLIENT' : True
            }
        """"
        self.__mqtt_settings = mqtt_settings

    def declare_device(self, device_name, device_type):
        # Declare the device in homie hierarchy - node / property
        pass



    def from_microbit(self, linemsg):
        msg = parse_line(linemsg)

        # Interpret measurement, Convert fields and tags to Homie device update
