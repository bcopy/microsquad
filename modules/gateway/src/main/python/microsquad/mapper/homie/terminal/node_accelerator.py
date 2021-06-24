import logging

from homie.node.property.property_integer import Property_Integer
from homie.node.node_base import Node_Base

logger = logging.getLogger(__name__)

class Node_Accelerator(Node_Base):
    _instance_count = 1

    def __init__(
        self,
        device,
        id = "accelerator",
        name = "Accelerator",
        type_="accelerator",
        retain=True,
        qos=1
    ):
      super().__init__(device, id, name, type_, retain, qos)

      self.add_property(Property_Integer(self, id="x", name="x", settable=False))
      self.add_property(Property_Integer(self, id="y", name="y", settable=False))
      self.add_property(Property_Integer(self, id="z", name="z", settable=False))
      

