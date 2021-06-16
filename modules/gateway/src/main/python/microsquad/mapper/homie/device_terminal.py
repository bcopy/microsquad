#!/usr/bin/env python
 
import logging

from homie.device_status import Device_Status
from homie.node.property.property_string import Property_String
from homie.node.property.property_temperature import Property_Temperature


logger = logging.getLogger(__name__)


class Device_Terminal(Device_Status):
    def __init__( self, device_id=None, name=None, homie_settings=None, mqtt_settings=None):
        super().__init__(device_id, name, homie_settings, mqtt_settings)

    def register_status_properties(self, node):
        self.temperature =  Property_Temperature(node, unit="C")
        node.add_property(self.temperature)

    def update_temperature(self, temperature):
        logger.info("Updated Temperature {}".format(temperature))
        self.temperature.value = temperature