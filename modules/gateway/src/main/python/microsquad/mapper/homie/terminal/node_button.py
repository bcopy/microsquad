import logging

from homie.node.property.property_string import Property_String
from homie.node.property.property_datetime import Property_DateTime
from homie.node.property.property_integer import Property_Integer
from homie.node.node_base import Node_Base

logger = logging.getLogger(__name__)

class Node_Button(Node_Base):
    _instance_count = 1

    def __init__(
        self,
        device,
        id,
        name,
        type_="button",
        retain=True,
        qos=1
    ):
      super().__init__(device, id, name, type_, retain, qos)

      self.add_property(Property_String(self,   id="pressed",        name="pressed"))
      self.add_property(Property_Integer(self,  id="pressed-count",  name="pressed count", settable=False))
      self.add_property(Property_DateTime(self, id="pressed-last",   name="pressed-last"))
      

