
import logging
import threading
from microsquad.event import EventType, MicroSquadEvent, EVENTS_GAME, EVENTS_SENSOR

from rx3 import Observable
from rx3.operators import filter

import importlib


from microsquad.game.abstract_game import AGame
from microsquad.mapper.homie.gateway.device_gateway import DeviceGateway

logger = logging.getLogger(__name__)

class GameManager():
    """
    A Game Manager instantiates and controls the lifecycle of games. It also propagate relevant
    events (e.g. from terminal sensors) to the currently running game.
    """

    def __init__(self, event_source: Observable, device_gateway: DeviceGateway):
        self._thread_terminate = True
        self._event_source = event_source
        self._device_gateway = device_gateway
        self._event_source.pipe(
            filter(lambda e: e.event_type in EVENTS_GAME)
        ).subscribe(
            on_next = self.handle_game_events
        )

        self._current_game : AGame = None
        
        self._event_source.pipe(
            filter(lambda e: e.event_type in EVENTS_SENSOR)
        ).subscribe(
            on_next = self.forward_sensor_events
        )

    def handle_game_events(self, event:MicroSquadEvent) -> None:
        if(event.event_type == EventType.GAME_START):
            # Locate the Game in the microsquad.game module and connect it to the event source
            # The game is expected under microsquad.game.<my_game_name>.<my_game_name>.Game
            GameClass = getattr(importlib.import_module("microsquad.game."+event.payload+"."+event.payload), "Game")
            # Instantiate the class (pass arguments to the constructor, if needed)
            self._current_game = GameClass(self._event_source, self._device_gateway)
            self._current_game.start()
            self._device_gateway.game_node.get_property("game-status").value = "RUNNING"
        elif(event.event_type == EventType.GAME_STOP):
            if(self._current_game is not None):
              self._current_game.stop()
              self._device_gateway.game_node.get_property("game-status").value = "STOPPED"
              self._current_game = None
        elif(event.event_type == EventType.GAME_TRANSITION):
            if(self._current_game is not None):
                if(event.payload in self._current_game.get_available_transitions()):
                    self._current_game.fire_transition(event.payload)
        elif(event.event_type == EventType.GAME_TRANSITIONS_UPDATED):
            if(self._current_game is not None and event.payload is not None):
                self._device_gateway.game_node.get_property("transitions").value = ",".join(event.payload)

    def forward_sensor_events(self, event:MicroSquadEvent) -> None:
        if(self._current_game is not None):
            self._current_game.process_event(event)
        

    @property
    def current_game(self):
        return self._current_game  
        
