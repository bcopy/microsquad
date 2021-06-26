from microsquad.mapper.homie.gateway.device_gateway import DeviceGateway

import unittest

class SimpleTest(unittest.TestCase):
    def setUp(self):
        mqtt_settings = {
            'MQTT_BROKER' : 'localhost',
            'MQTT_PORT' : 1883,
        }
        self.gateway = DeviceGateway(mqtt_settings=mqtt_settings)
        self.gateway.start()

    def test_add_player(self):
        self.gateway.player_manager.add_player("01")
        self.assertIsNotNone(self.gateway.get_node("player-01"))
        self.assertIsNone(self.gateway.get_node("player-02"))
        self.gateway.player_manager.add_player("02")
        self.assertIsNotNone(self.gateway.get_node("player-02"))
        self.assertIsNotNone(self.gateway.get_node("player-02").get_property("nickname"))
        self.assertIsNotNone(self.gateway.get_node("player-02").get_property("skin"))

    def test_add_remove_teams(self):
        self.gateway.team_manager.add_team("blue")
        self.assertEqual(self.gateway.team_manager.get_property("list").value,'["blue"]')
        self.gateway.team_manager.remove_team("blue")
        self.assertEqual(self.gateway.team_manager.get_property("list").value,'[]')
        
    def test_add_remove_player_to_team(self):
        self.gateway.player_manager.add_player("susan")
        self.gateway.player_manager.add_player("roger")
        self.gateway.team_manager.add_team("orange")
        self.assertIsNotNone(self.gateway.get_node("team-orange"))
        self.gateway.team_manager.add_player("orange:susan")
        self.assertEqual(self.gateway.team_manager.get_property("list").value,'["orange"]')
        self.assertEqual(self.gateway.team_manager.get_property("list-players").value,'{"orange":["susan"]}')
        self.gateway.team_manager.add_player("orange:roger")
        self.assertEqual(self.gateway.team_manager.get_property("list-players").value,'{"orange":["susan","roger"]}')
        self.gateway.team_manager.remove_player("orange:susan")
        self.assertEqual(self.gateway.team_manager.get_property("list-players").value,'{"orange":["roger"]}')
        

if __name__ == '__main__':
    unittest.main()