from microsquad.mapper.homie.terminal.device_terminal import Device_Terminal

import unittest

class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.mqtt_settings = {
            'MQTT_BROKER' : 'localhost',
            'MQTT_PORT' : 1883,
        }
        self.terminals = []

    def test_add_terminal(self):
        terminal = Device_Terminal(device_id="terminal-01", name="Terminal 01", mqtt_settings=self.mqtt_settings)
        self.terminals.append(terminal)
        self.terminals[0].get_node("button-a").get_property("pressed").value = True
        self.assertTrue(self.terminals[0].get_node("button-a").get_property("pressed").value)


if __name__ == '__main__':
    unittest.main()