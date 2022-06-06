import logging

from homie.node.property.property_string import Property_String
from homie.node.property.property_datetime import Property_DateTime
from homie.node.property.property_integer import Property_Integer
from homie.node.property.property_color import Property_Color
from homie.node.node_base import Node_Base

logger = logging.getLogger(__name__)

class NodeTeam(Node_Base):
    _instance_count = 1

    def __init__(
        self,
        device,
        id="team",
        name="Team",
        type_="team",
        retain=True,
        qos=1
    ):
      super().__init__(device, id, name, type_, retain, qos)

      self.add_property(Property_String(self, id="nickname" , name="Nickname"))
      self.add_property(Property_String(self, id="players"  , name="Players"))
      self.add_property(Property_String(self, id="terminals", name="Terminals"))
      self.add_property(Property_String(self, id="say", name="Say"))
      self.add_property(Property_String(self, id="animation", name="Animation"))
      # hexadecimal color value (replace with Color Property when implemented in Homie lib)
      self.add_property(Property_String(self, id="color", name="Color")) 

