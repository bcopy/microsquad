#!/usr/bin/env python
 
import logging

from homie.device_base import Device_Base
from homie.node.property.property_string import Property_String
from homie.node.property.property_temperature import Property_Temperature
from rx3 import Observable


from ....event import EventType,MicroSquadEvent

from .node_accelerator import NodeAccelerator
from .node_button import NodeButton
from .node_display import NodeDisplay
from .node_temperature import NodeTemperature
from .node_vote import NodeVote
from .node_info import NodeInfo

logger = logging.getLogger(__name__)


class DeviceTerminal(Device_Base):
    def __init__( self, event_source : Observable, device_id=None, name=None, homie_settings=None, mqtt_settings=None):
        super().__init__(device_id, name, homie_settings, mqtt_settings)

        self.add_node(NodeAccelerator(self))
        self.add_node(NodeButton(self,id="button-a",name="Button A"))
        self.add_node(NodeButton(self,id="button-b",name="Button B"))
        self.add_node(NodeDisplay(self))
        self.add_node(NodeTemperature(self))
        self.add_node(NodeVote(self))
        self.add_node(NodeInfo(self, command_handler= self.update_command))

        self._event_source = event_source
        if self._event_source is None:
            raise ValueError("Terminal must be passed an event source.")

    def update_command(self, command):
        self._event_source.on_next(MicroSquadEvent(EventType.TERMINAL_COMMAND,command))

   

