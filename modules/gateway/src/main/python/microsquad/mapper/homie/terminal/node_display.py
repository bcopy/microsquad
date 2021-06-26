import logging

from homie.node.property.property_string import Property_String
from homie.node.property.property_dimmer import Property_Dimmer
from homie.node.node_base import Node_Base

logger = logging.getLogger(__name__)

class NodeDisplay(Node_Base):
    def __init__(
        self,
        device,
        id = "display",
        name = "Display",
        type_="display",
        retain=True,
        qos=1
    ):
      super().__init__(device, id, name, type_, retain, qos)

      self.add_property(Property_String(self, id="contents", name="contents", settable=False))
      self.add_property(Property_Dimmer(self, id="luminosity", name="luminosity", settable=False))
      

