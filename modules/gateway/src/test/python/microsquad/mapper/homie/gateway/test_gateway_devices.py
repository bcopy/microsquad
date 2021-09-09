from microsquad.event import MicroSquadEvent,EventType
from microsquad.mapper.homie.gateway.device_gateway import DeviceGateway

import unittest

from rx3.subject import Subject

class TestGatewayDevice(unittest.TestCase):
    def setUp(self):
        mqtt_settings = {
            'MQTT_BROKER' : 'localhost',
            'MQTT_PORT' : 1883,
        }
        self.event_source = Subject()
        self.gateway = DeviceGateway(event_source=self.event_source,mqtt_settings=mqtt_settings)

    def test_add_player(self):
        self.gateway._player_manager.add_player("01")
        assert self.gateway.get_node("player-01") is not None
        assert self.gateway.get_node("player-02") is None
        self.gateway._player_manager.add_player("02")
        assert self.gateway.get_node("player-02") is not None
        assert self.gateway.get_node("player-02").get_property("nickname") is not None
        assert self.gateway.get_node("player-02").get_property("skin") is not None
        assert self.gateway.get_node("player-02").get_property("order") is not None
        assert self.gateway.get_node("player-01").get_property("order").value == 0
        assert self.gateway.get_node("player-02").get_property("order").value == 1

    def test_add_remove_teams(self):
        self.gateway._team_manager.add_team("blue")
        assert self.gateway._team_manager.get_property("list").value == '["blue"]'
        self.gateway._team_manager.remove_team("blue")
        assert self.gateway._team_manager.get_property("list").value == '[]'
        
    def test_add_remove_player_to_team(self):
        self.gateway._player_manager.add_player("susan")
        self.gateway._player_manager.add_player("roger")
        self.gateway._team_manager.add_team("orange")
        assert self.gateway.get_node("team-orange") is not None
        self.gateway._team_manager.add_player("orange:susan")
        assert self.gateway._team_manager.get_property("list").value == '["orange"]'
        assert self.gateway._team_manager.get_property("list-players").value == '{"orange":["susan"]}'
        self.gateway._team_manager.add_player("orange:roger")
        assert self.gateway._team_manager.get_property("list-players").value == '{"orange":["susan","roger"]}'
        self.gateway._team_manager.remove_player("orange:susan")
        assert self.gateway._team_manager.get_property("list-players").value == '{"orange":["roger"]}'
        
    def test_broadcast_event(self):
        received_events: MicroSquadEvent = []
        subscriber = self.event_source.subscribe(on_next = lambda evt: received_events.append(evt) )
        self.gateway.update_broadcast("buttons")
        assert 1 == len(received_events)
        assert EventType.TERMINAL_BROADCAST == received_events[0].event_type
        assert received_events[0].device_id is None
        

if __name__ == '__main__':
    unittest.main()