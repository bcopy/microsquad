import unittest

from rx3 import Observable
from microsquad.mapper.homie.homie_mapper  import HomieMapper
from microsquad.mapper.homie.gateway.device_gateway import DeviceGateway

class SimpleTest(unittest.TestCase):
    def setUp(self):
        mqtt_settings = {
            'MQTT_BROKER' : 'localhost',
            'MQTT_PORT' : 1883,
        }
        self.gateway = DeviceGateway(mqtt_settings=mqtt_settings)

        self.event_source = Observable.create()
        self.mapper = HomieMapper(self.gateway,self.event_source)
        self.gateway.start()

    def test_bonjour_event(self):
        received_events = []
        subscriber = self.event_source.subscribe(lambda evt: received_events.append(evt) )
        self.mapper.map_from_microbit("bonjour dev_id=1234")
        self.assertTrue(len(received_events) > 0)

if __name__ == '__main__':
    unittest.main()