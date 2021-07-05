import unittest
from microsquad.event import EventType, MicroSquadEvent

import rx3
from microsquad.mapper.homie.homie_mapper import HomieMapper
from microsquad.mapper.homie.gateway.device_gateway import DeviceGateway
from rx3.subject import Subject

class TestHomieMapper(unittest.TestCase):
    def setUp(self):
        _mqtt_settings = {
            'MQTT_BROKER' : 'localhost',
            'MQTT_PORT' : 1883,
        }
        self.received_events: MicroSquadEvent = []
        self.event_source = Subject()
        self.gateway = DeviceGateway(event_source = self.event_source,mqtt_settings=_mqtt_settings)

        self.mapper = HomieMapper(self.gateway,self.event_source)
        self.subscriber = self.event_source.subscribe(on_next = lambda evt: self.received_events.append(evt) )
        
        self.gateway.start()

    def test_bonjour_event(self):
        dev_id = "1234-5678"
        self.mapper.map_from_microbit('bonjour dev_id="{}"'.format(dev_id))
        self.assertEqual(1,len(self.received_events))
        self.assertEqual(EventType.BONJOUR, self.received_events[0].event_type)
        self.assertEqual(dev_id, self.received_events[0].device_id)

    def test_read_accelerator_event(self):
        dev_id = "1234-5678"
        readings = {'x':-12,'y':80,'z':-60}
        self.mapper.map_from_microbit('read_accel,x={x},y={y},z={z} dev_id="{0}"'.format(dev_id,**readings))
        self.assertEqual(1,len(self.received_events))
        for evt in self.received_events:
          self.assertEqual(EventType.ACCELERATOR, evt.event_type)
          self.assertEqual(dev_id, evt.device_id)
        for k in readings:
          self.assertEqual(readings[k], int(self.received_events[0].payload[k]))


if __name__ == '__main__':
    unittest.main()