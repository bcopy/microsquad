#!/usr/bin/env python
 
import logging

from homie.device_base import Device_Base

from homie.node.property.property_string import Property_String
from homie.node.node_base import Node_Base

from .node_player_manager import Node_Player_Manager

from .node_team_manager import Node_Team_Manager

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

        self.scoreboard = Node_Base(self,id="scoreboard", name="Scoreboard", type_="scoreboard")
        self.add_node(self.scoreboard)
        self.scoreboard.add_property(Property_String(node = self.scoreboard, id="score",name="score" ))

        self.player_manager = Node_Player_Manager(self)
        self.add_node(self.player_manager)

        self.team_manager = Node_Team_Manager(self)
        self.add_node(self.team_manager)

        self.game = Node_Base(self,id="game", name="game", type_="game")
        self.add_node(self.game)
        self.game.add_property(Property_String(node = self.game, id="script",name="script" ))
        self.game.add_property(Property_String(node = self.game, id="audience-code",name="audience-code" ))
        self.game.add_property(Property_String(node = self.game, id="admin-code",name="admin-code" ))

    # def update_score(self,score):
    #     logger.debug("Score update {}".format(score))
