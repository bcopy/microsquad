#!/usr/bin/env python
 
import logging

from homie.device_base import Device_Base
from homie.node.property.property_string import Property_String
from homie.node.property.property_temperature import Property_Temperature

from .node_accelerator import Node_Accelerator
from .node_button import Node_Button
from .node_display import Node_Display
from .node_temperature import Node_Temperature
from .node_vote import Node_Vote
from .node_info import Node_Info

logger = logging.getLogger(__name__)


class Device_Terminal(Device_Base):
    def __init__( self, device_id=None, name=None, homie_settings=None, mqtt_settings=None):
        super().__init__(device_id, name, homie_settings, mqtt_settings)

        self.add_node(Node_Accelerator(self))
        self.add_node(Node_Button(self,id="button-a",name="Button A"))
        self.add_node(Node_Button(self,id="button-b",name="Button B"))
        self.add_node(Node_Display(self))
        self.add_node(Node_Temperature(self))
        self.add_node(Node_Vote(self))
        self.add_node(Node_Info(self))

   

