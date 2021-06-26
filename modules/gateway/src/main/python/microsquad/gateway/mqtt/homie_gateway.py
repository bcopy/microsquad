import paho.mqtt.client as mqtt

import logging

from rx3 import operators,Observable

from ...mapper.homie.gateway.device_gateway import DeviceGateway
from ...mapper.homie.homie_mapper import HomieMapper
from ...connector.bitio_connector import BitioConnector

class HomieGateway:
    MQTT_SETTINGS = {
        'MQTT_BROKER' : 'localhost',
        'MQTT_PORT' : 1883,
    }

    """
    MicroSquad Gateway MQTT Homie implementation.
    Using provided MQTT connection parameters, this gateway declares a series of Homie devices on the MQTT broker
    that can be used to interact with MicroSquad entities (players, terminals, teams, scoreboard etc...).
    Remote method calls are implemented as Homie settable properties.
    Events are propagated using RxPy.
    """
    def __init__(self):
        self._event_source = Observable.create()
        self._homie_settings = {
            "topic": self._homie_root_topic,
            "update_interval": 1
        }
        self._gateway = DeviceGateway(event_source = self._event_source, homie_settings=self._homie_settings,mqtt_settings=HomieGateway.MQTT_SETTINGS)
        self._mapper = HomieMapper(self._gateway, self._event_source)
        self._connector = BitioConnector(self._mapper)

    def start(self):
        self._gateway.start()
        self._connector.start()

 