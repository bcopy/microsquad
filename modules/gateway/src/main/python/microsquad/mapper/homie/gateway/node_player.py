import logging

from homie.node.property.property_string import Property_String
from homie.node.property.property_datetime import Property_DateTime
from homie.node.property.property_integer import Property_Integer
from homie.node.node_base import Node_Base

logger = logging.getLogger(__name__)

class Node_Player(Node_Base):
    _instance_count = 1

    def __init__(
        self,
        device,
        id="player",
        name="Player",
        type_="player",
        retain=True,
        qos=1
    ):
      super().__init__(device, id, name, type_, retain, qos)

      self.add_property(Property_String(self,   id="nickname",           name="nickname"))
      self.add_property(Property_String(self,   id="skin",               name="skin"))
      self.add_property(Property_String(self,   id="say",                name="say"))
      self.add_property(Property_DateTime(self, id="say-start",          name="say start"))
      self.add_property(Property_Integer(self,  id="say-duration",       name="say duration", settable=False))
      self.add_property(Property_String(self,   id="animation",          name="animation"))
      self.add_property(Property_DateTime(self, id="animation-start",    name="animation start"))
      self.add_property(Property_Integer(self,  id="animation-duration", name="animation duration", settable=False))
      self.add_property(Property_String(self,   id="accessory",          name="accessory"))
      self.add_property(Property_String(self,   id="terminal-id",        name="terminal id"))

