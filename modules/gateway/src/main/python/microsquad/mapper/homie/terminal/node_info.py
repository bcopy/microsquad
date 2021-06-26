import logging

from homie.node.property.property_string import Property_String
from homie.node.property.property_datetime import Property_DateTime
from homie.node.node_base import Node_Base

logger = logging.getLogger(__name__)

class NodeInfo(Node_Base):
    def __init__(
        self,
        device,
        id = "info",
        name = "Info",
        type_="info",
        retain=True,
        qos=1
    ):
      super().__init__(device, id, name, type_, retain, qos)

      self.add_property(Property_String(self, id="terminal-id",   name="Terminal ID"))
      self.add_property(Property_String(self, id="serial-number", name="Serial Number"))
      self.add_property(Property_DateTime(self, id="heartbeat", name="Heartbeat"))
      