#!/usr/bin/env python
 
import logging

from homie.device_base import Device_Base

from homie.node.property.property_string import Property_String
from homie.node.node_base import Node_Base

from .node_player_manager import NodePlayerManager

from .node_team_manager import NodeTeamManager

logger = logging.getLogger(__name__)


class DeviceGateway(Device_Base):
    """
    The Gateway device exposes properties of the microsquad gateway.

    It can be used to read properties of the ongoing game, players and teams currently active.
    """
    
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

        self.player_manager = NodePlayerManager(self)
        self.add_node(self.player_manager)

        self.team_manager = NodeTeamManager(self)
        self.add_node(self.team_manager)

        self.game = Node_Base(self,id="game", name="game", type_="game")
        self.add_node(self.game)
        self.game.add_property(Property_String(node = self.game, id="script",name="script" ))
        self.game.add_property(Property_String(node = self.game, id="audience-code",name="audience-code" ))
        self.game.add_property(Property_String(node = self.game, id="admin-code",name="admin-code" ))

