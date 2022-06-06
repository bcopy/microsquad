import unittest
from microsquad.event import EventType, MicroSquadEvent

import rx3
from microsquad.mapper.homie.homie_mapper import HomieMapper
from microsquad.mapper.homie.gateway.device_gateway import DeviceGateway
from rx3.subject import Subject

import logging
logging.getLogger('homie').setLevel(logging.WARN)

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
        dev_id = "12345678"
        self.mapper.map_from_microbit('bonjour,dev_id={}'.format(dev_id))
        bonjour_events = list(filter(lambda evt: evt.event_type == EventType.BONJOUR, self.received_events))
        assert 1 == len(bonjour_events)
        assert dev_id == bonjour_events[0].device_id

    def test_read_accelerator_event(self):
        dev_id = "1234-5678"
        readings = {'x':-12,'y':80,'z':-60}
        self.mapper.map_from_microbit('read_accel,x={x},y={y},z={z},dev_id="{0}"'.format(dev_id,**readings))
        accel_events = list(filter(lambda evt: evt.event_type == EventType.ACCELERATOR, self.received_events))
        assert 1 == len(accel_events)
        for evt in accel_events:
          assert dev_id == evt.device_id
        for k in readings:
          assert readings[k] == int(accel_events[0].payload[k])


if __name__ == '__main__':
    unittest.main()