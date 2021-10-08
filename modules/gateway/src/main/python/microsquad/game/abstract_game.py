from abc import ABCMeta,abstractmethod

import logging
import threading
import enum

from homie.node.property.property_base import Property_Base
from microsquad.event import EventType, MicroSquadEvent

from ..mapper.homie.gateway.device_gateway import DeviceGateway
from rx3 import Observable

logger = logging.getLogger(__name__)

@enum.unique
class EMOTE(enum.Enum):
    HEART = ("heart",0, "&#10084;")
    SAD = ("sad",1, "&#128542;")
    HAPPY = ("happy",2, "&#128512;")
    SKULL = ("skull",3, "&#128565;")

    def __init__(self, id:str,idx:int, entity:str) -> None:
        self.id = id
        self.idx = idx
        self.entity = entity
    
    def equals(self, string) -> bool:
       return self.value == string

def find_emote_by_idx(idx:int) -> EMOTE:
    return next((emote for emote in list(EMOTE) if emote.idx == idx), None)

def find_emote_by_ide(id:str) -> EMOTE:
    return next((emote for emote in list(EMOTE) if emote.id == id), None)

class AGame(metaclass=ABCMeta):
    """
    Base class for MicroSquad games
    """
    
    def __init__(self, event_source: Observable, gateway : DeviceGateway) -> None:
        self._event_source = event_source
        self._device_gateway = gateway
        self._available_transitions : list = []
        self._last_fired_transition = None

    @abstractmethod
    def process_event(self, event:MicroSquadEvent) -> None:
        """
        Handle the next game event
        """
        pass
        
    @abstractmethod
    def start(self) -> None:
        pass

    def stop(self) -> None:
        logger.debug("Game {} now stopped.".format(__name__))

    def fire_transition(self, transition) -> None:
        self._last_fired_transition = transition

    @property
    def last_fired_transition(self):
        return self._last_fired_transition

    @property
    def event_source(self):
        return self._event_source

    @property
    def device_gateway(self):
        return self._device_gateway

    def get_all_player_nodes(self) -> list:
        return filter(lambda node : node.id.startswith("player-"), self._device_gateway.nodes.values())

    def get_available_transitions_as_strings(self) -> list:
        return [t.value for t in self._available_transitions]

    def update_available_transitions(self,transitions:list) -> None:
        # TODO Add transition validation and/or transformation to JSON format
        self._available_transitions = transitions
        self.event_source.on_next(MicroSquadEvent(EventType.GAME_TRANSITIONS_UPDATED,payload=[t.value for t in self._available_transitions]))

def set_next_in_collection(property: Property_Base, collection) -> None:
    idx = 0
    current_value = property.value
    if(current_value in collection):
        idx = collection.index(current_value) +1
    if(idx >= len(collection)) :
        idx = 0
    property.value = collection[idx]

def set_prev_in_collection(property: Property_Base, collection) -> None:
    idx = 0
    current_value = property.value
    if(current_value in collection):
        idx = collection.index(current_value) -1
    if(idx < 0) :
        idx = len(collection)-1
    property.value = collection[idx]
