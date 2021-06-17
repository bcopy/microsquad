from line_protocol_parser import parse_line, LineFormatError

from homie.device_status import Device_Status
from homie.node.property import property_string

from .homie import Device_Gateway, Device_Terminal

import logging

from . import AbstractMapper

"""
Homie V4 Mapper - converts incoming MQTT messages and outgoing Microbit radio messages to Homie devices, nodes and properties.
"""
class HomieMapper(AbstractMapper):

    def __init__(self, homie_root_topic, mqtt_settings):
        self._homie_root_topic = homie_root_topic

        self._homie_settings = {
            "topic": self._homie_root_topic,
            "update_interval": 1
        }
        self._mqtt_settings = mqtt_settings
        self._gateway = Device_Gateway(homie_settings=self._homie_settings,mqtt_settings=self._mqtt_settings)
        self._terminals = []

    def declare_terminal_if_required(self):
        
        self._terminals.append()


    def map_from_mqtt(self, message):
        # Interpret incoming MQTT update and create required devices
        """
        /player-manager/add
        /player/manager/remove
        """
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


