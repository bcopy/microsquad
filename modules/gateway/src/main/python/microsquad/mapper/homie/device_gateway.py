#!/usr/bin/env python
 
import logging

import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

from homie.device_base import Device_Base

from homie.node.property.property_string import Property_String
from homie.node.node_base import Node_Base

logger = logging.getLogger(__name__)


class Device_Gateway(Device_Base):
    __instances_count = 0

    def __init__(
        self,
        device_id="usquad-gateway",
        name="MicroSquad Gateway",
        homie_settings=None,
        mqtt_settings=None
    ):
        if device_id == "usquad-gateway":
            Device_Gateway.__instances_count += 1
            device_id = device_id+str(Device_Gateway.__instances_count)
        super().__init__(device_id, name, homie_settings, mqtt_settings)

        self.node_scoreboard = Node_Base(self,id="scoreboard", name="Scoreboard", type_="scoreboard")
        self.add_node(self.node_scoreboard)
        self.node_scoreboard.add_property(Property_String(node = self.node_scoreboard, id="score",settable=True, name="Score", set_value = self.set_score ))
        self.start()

    def set_score(self,score):
        logger.info("Score set to {}".format(score))

    def update_score(self,score):
        logger.debug("Score update {}".format(score))
        self.get_node("scoreboard").get_property("score").value = score
