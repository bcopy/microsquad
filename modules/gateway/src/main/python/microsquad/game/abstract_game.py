from abc import ABCMeta,abstractmethod

import logging
import threading

from homie.node.property.property_base import Property_Base
from microsquad.event import EventType, MicroSquadEvent

from ..mapper.homie.gateway.device_gateway import DeviceGateway
from rx3 import Observable

logger = logging.getLogger(__name__)

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
