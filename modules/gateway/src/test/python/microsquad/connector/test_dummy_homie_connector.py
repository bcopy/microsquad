import unittest

import time
from microsquad.event import EventType, MicroSquadEvent

import microsquad.gateway.dummy.dummy_gateway as dummy

import logging
logging.getLogger('homie').setLevel(logging.WARN)

DEVICE_ID = '12546-4656'


class TestDummyHomieConnector(unittest.TestCase):
    """ 
    Test that simulated incoming microbit messages are properly parsed into Device / Node / Properties
    """

    def setUp(self) -> None:
        dummy.main()
        dummy.gateway.connector.simulate_message("bonjour,dev_id={}".format(DEVICE_ID))
        # Wait for the message to be processed
        time.sleep(0.1)
        return super().setUp()

    def test_bonjour_message(self):
        assert dummy.gateway.deviceGateway.terminals[DEVICE_ID] is not None

    def test_button_read(self):
        assert dummy.gateway.deviceGateway.terminals[DEVICE_ID].get_node("button-a").get_property("pressed").value == 0
        dummy.gateway.connector.simulate_message("read_button,button=\"a\",dev_id=\"{}\" 123456978".format(DEVICE_ID))
        time.sleep(1)
        assert dummy.gateway.deviceGateway.terminals[DEVICE_ID].get_node("button-a").get_property("pressed").value == 1
    
    def test_accel_read(self):
        assert dummy.gateway.deviceGateway.terminals[DEVICE_ID].get_node("accel").get_property("x").value is None

        dummy.gateway.connector.simulate_message("read_accel,x=500,y=300,z=-823,dev_id={} 123456978".format(DEVICE_ID))
        time.sleep(1)
        assert dummy.gateway.deviceGateway.terminals[DEVICE_ID].get_node("accel").get_property("x").value == 500

    def test_vote_read(self):
        assert dummy.gateway.deviceGateway.terminals[DEVICE_ID].get_node("vote").get_property("value").value is None
        dummy.gateway.connector.simulate_message("read_vote,value=\"elephant\",index=3,dev_id={} 123456978".format(DEVICE_ID))
        time.sleep(2)
        assert dummy.gateway.deviceGateway.terminals[DEVICE_ID].get_node("vote").get_property("value").value == 'elephant'

    def test_handle_rxpy_broadcast(self):
        # Test that the AbstractConnector handles TERMINAL_BROADCAST events as expected
        dummy.gateway.event_source.on_next(MicroSquadEvent(EventType.TERMINAL_BROADCAST,payload="buttons"))
        # ... it should emerge out of the connector
        assert dummy.gateway.connector.last_sent=="buttons"


if __name__ == '__main__':
    unittest.main()