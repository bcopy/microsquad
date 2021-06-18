import logging

from homie.node.property.property_string import Property_String
from homie.node.node_base import Node_Base

from .node_player import Node_Player

logger = logging.getLogger(__name__)

class Node_Player_Manager(Node_Base):

    def __init__(self, device):
      super().__init__(device, id="player-manager", name="Player Manager", type_="player_manager", retain=True, qos=1)
      
      self.add_property(Property_String(self, id="add", settable=True, name="add", set_value = self.add_player ))
      self.add_property(Property_String(self, id="remove", settable=True, name="remove", set_value = self.remove_player ))

      self.players = []
      self.add_property(Property_String(self, id="list", name="list" ))
    
    def remove_player(self,identifier):
        logger.info("Removing Player : {}".format(identifier))
        # TODO : If the identifier is not a valid node id, look up the nickname in a mapping table
        # TODO : create the mapping table ;-)pp
        self.device.remove_node(identifier)

    def add_player(self,identifier):
        """
            TODO : Split the identifier either: 
                - id
                - id:name 
                - id:name:nickname
                - or empty (random UUID)
        """
        self.device.add_node(Node_Player(self.device,id=identifier, name=identifier))
        self.players.append(identifier)
        self.get_property("list").value = ",".join(self.players)
        logger.info("Player Added : {}".format(identifier))
