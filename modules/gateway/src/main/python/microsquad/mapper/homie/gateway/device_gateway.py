#!/usr/bin/env python
 
import logging

from homie.device_base import Device_Base

from homie.node.property.property_string import Property_String
from homie.node.node_base import Node_Base

from .node_player import Node_Player
from .node_player_manager import Node_Player_Manager

logger = logging.getLogger(__name__)


class Device_Gateway(Device_Base):
    
    def __init__(
        self,
        device_id= "usquad-gateway",
        name="MicroSquad Gateway",
        homie_settings=None,
        mqtt_settings=None
    ):
        super().__init__(device_id, name, homie_settings, mqtt_settings)

        scoreboard = Node_Base(self,id="scoreboard", name="Scoreboard", type_="scoreboard")
        self.add_node(scoreboard)
        scoreboard.add_property(Property_String(node = scoreboard, id="score",settable=True, name="score", set_value = self.set_score ))

        self.player_manager = Node_Player_Manager(self)
        self.add_node(self.player_manager)
        
        self.player_manager.add_player("player-01")

        self.start()

    def set_score(self,score):
        logger.info("Score set to {}".format(score))

    def update_score(self,score):
        logger.debug("Score update {}".format(score))
        self.get_node("scoreboard").get_property("score").value = score
