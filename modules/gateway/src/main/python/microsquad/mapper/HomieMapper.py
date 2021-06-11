from line_protocol_parser import parse_line, LineFormatError

from homie.device_status import Device_Status
from homie.node.property import property_string

import logging

from . import AbstractMapper

"""
Homie V4 Mapper - converts incoming MQTT messages and outgoing Microbit radio messages to Homie devices, nodes and properties.
"""
class HomieMapper(AbstractMapper):

    def __init__(self, homie_root_topic, mqtt_settings):
        self.__homie_root_topic = homie_root_topic

        """ mqtt_settings = {
            'MQTT_BROKER' : 'your.mqtt.server',
            'MQTT_PORT' : 1883,
            'MQTT_SHARE_CLIENT' : True
            }
        """
        self.__mqtt_settings = mqtt_settings

    def declare_device(self, device_name, device_type):
        # Declare the device in homie hierarchy - node / property
        pass

    def map_to_mqtt(self, message):
        pass
    
    def map_from_microbit(self, message):
        try:
            msg = parse_line(message)
            measurement = msg.measurement

            # Interpret measurement, Convert fields and tags to Homie device update
            if measurement.startswith("read_"):
                # Propagate the read on the corresponding device property
                if measurement.startswith("read_button"):
                    # A or B ?
                    # Propagate an update on the device property
                    # get 
                    pass
                if measurement =="read_accel":
                    # Propagate an update on the device property
                    # get tags x, y, z
                    pass
                if measurement =="read_vote":
                    # Propagate an update on the device property
                    # get tags value, index
                    pass
        except LineFormatError:
            logging.exception("Received invalid line message : %s",message)
        except:
             logging.exception("Unexpected error on line message : %s",message)


