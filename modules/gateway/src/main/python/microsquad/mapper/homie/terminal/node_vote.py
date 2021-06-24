import logging

from homie.node.property.property_string import Property_String
from homie.node.property.property_datetime import Property_DateTime
from homie.node.node_base import Node_Base

logger = logging.getLogger(__name__)

class Node_Vote(Node_Base):
    _instance_count = 1

    def __init__(
        self,
        device,
        id = "vote",
        name = "Vote",
        type_="vote",
        retain=True,
        qos=1
    ):
      super().__init__(device, id, name, type_, retain, qos)

      self.add_property(Property_String(self,   id="choice",        name="choice"))
      self.add_property(Property_DateTime(self, id="vote-last",   name="vote-last"))
      