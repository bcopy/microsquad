import unittest

from rx3.subject import Subject

import logging
import time

from microsquad.game.game_manager import GameManager
from microsquad.event import MicroSquadEvent
from microsquad.mapper.homie.gateway.device_gateway import DeviceGateway
from microsquad.event import EventType
from microsquad.game.my_test_game.my_test_game import Game as TestGame

logging.getLogger('homie').setLevel(logging.WARN)

class TestGameManager(unittest.TestCase):
    def setUp(self) -> None:
       _mqtt_settings = {
           'MQTT_BROKER' : 'localhost',
           'MQTT_PORT' : 1883,
       }
       self.received_events: MicroSquadEvent = []
       self.event_source = Subject()
       self.gateway = DeviceGateway(event_source = self.event_source,mqtt_settings=_mqtt_settings)
       self.game_manager = GameManager(self.event_source, self.gateway)
       return super().setUp()
    
    def test_game_start_stop_via_rxpy(self):
        self.event_source.on_next(MicroSquadEvent(EventType.GAME_START, payload="my_test_game"))
        time.sleep(0.5)
        test_game = self.game_manager.current_game
        assert isinstance(test_game,TestGame)
        self.event_source.on_next(MicroSquadEvent(EventType.BUTTON, payload={"pressed":1,"count":1}))
        self.event_source.on_next(MicroSquadEvent(EventType.BUTTON, payload={"pressed":1,"count":2}))
        self.event_source.on_next(MicroSquadEvent(EventType.BUTTON, payload={"pressed":0,"count":2}))
        time.sleep(0.5)
        assert len(test_game.received_events)==3
        self.event_source.on_next(MicroSquadEvent(EventType.GAME_STOP))
        time.sleep(0.3)
        assert self.game_manager.current_game is None

    def test_game_start_stop_via_device_gateway(self):
        self.gateway.update_game("my_test_game")
        time.sleep(0.5)
        test_game = self.game_manager.current_game
        assert isinstance(test_game,TestGame)
        self.event_source.on_next(MicroSquadEvent(EventType.BUTTON, payload={"pressed":1,"count":1}))
        self.event_source.on_next(MicroSquadEvent(EventType.BUTTON, payload={"pressed":1,"count":2}))
        self.event_source.on_next(MicroSquadEvent(EventType.BUTTON, payload={"pressed":0,"count":2}))
        time.sleep(0.5)
        assert len(test_game.received_events)==3
        self.gateway.update_game("")
        time.sleep(0.3)
        assert self.game_manager.current_game is None
        
        
        


        



if __name__ == '__main__':
    unittest.main()
