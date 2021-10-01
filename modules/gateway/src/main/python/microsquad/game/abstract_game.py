from abc import ABCMeta,abstractmethod

import logging
import threading
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
        self._available_transitions : str = []
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

    @abstractmethod
    def stop(self) -> None:
        pass

    def fire_transition(self, transition):
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

    @property
    def available_transitions(self):
        return self._available_transitions

    @available_transitions.setter
    def available_transitions(self,transitions):
        # TODO Add transition validation and/or transformation to JSON format
        self._available_transitions = transitions
        self.event_source.on_next(MicroSquadEvent(EventType.GAME_TRANSITIONS_UPDATED,payload=self._available_transitions))