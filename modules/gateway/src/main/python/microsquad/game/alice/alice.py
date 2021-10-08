import logging

from ..abstract_game import AGame, set_next_in_collection, set_prev_in_collection

import enum
from rx3 import Observable
from microsquad.event import EVENTS_SENSOR, EventType, MicroSquadEvent
from microsquad.mapper.homie.gateway.device_gateway import DeviceGateway


logger = logging.getLogger(__name__)

@enum.unique
class TRANSITIONS(enum.Enum):
  SIZE = "Size"
  ROTATE = "Rotate"
  def equals(self, string):
       return self.value == string

class Game(AGame):
    """ 
    A simple game that allows to declare new players and customize their appearance
    """
    def __init__(self, event_source: Observable, gateway : DeviceGateway) -> None:
        super().__init__(event_source, gateway)

    
    def start(self) -> None:
        print("Alice game starting")
        super().update_available_transitions(list(TRANSITIONS))
        super().fire_transition(TRANSITIONS.SIZE)
        super().device_gateway.update_broadcast("buttons")

    def fire_transition(self, transition) -> None:
        super().fire_transition(transition)

    def process_event(self, event:MicroSquadEvent) -> None:
        logger.debug("Alice game received event {} for device {}: {}".format(event.event_type.name, event.device_id, event.payload))
        self.device_gateway.get_node("players-manager").add_player(event.device_id)
        if event.event_type == EventType.BUTTON:
            transition =TRANSITIONS(self._last_fired_transition)
            if transition == TRANSITIONS.SIZE:
                if(event.event_type == EventType.BUTTON):
                  factor = 0.9
                  if event.payload["button"]=="b" :
                      factor = 1.1
                  self.device_gateway.get_node("player-"+event.device_id).get_property("scale").value *= factor
            if transition == TRANSITIONS.ROTATE:
                angle_modifier = -0.2
                if event.payload["button"]=="b" :
                    angle_modifier = 0.2
                self.device_gateway.get_node("player-"+event.device_id).get_property("rotation").value += angle_modifier

    