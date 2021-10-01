import paho.mqtt.client as mqtt

import logging

from rx3.subject import Subject

from ...game.game_manager import GameManager

from ...mapper.homie.gateway.device_gateway import DeviceGateway
from ...mapper.homie.homie_mapper import HomieMapper
from ...connector.bitio_connector import BitioConnector

class HomieBitioGateway:
    

    """
    MicroSquad Gateway MQTT Homie implementation.
    Using provided MQTT connection parameters, this gateway declares a series of Homie devices on the MQTT broker
    that can be used to interact with MicroSquad entities (players, terminals, teams, scoreboard etc...).
    Remote method calls are implemented as Homie settable properties.
    Events are propagated using RxPy.
    """
    def __init__(self, homie_settings, mqtt_settings, event_source):
        
        self._event_source = event_source
        self._homie_settings = homie_settings
        self._mqtt_settings = mqtt_settings
        self._gatewayDevice = DeviceGateway(event_source = self._event_source, homie_settings=self._homie_settings,mqtt_settings=self._mqtt_settings)
        self._mapper = HomieMapper(self._gatewayDevice, self._event_source)
        self._connector = BitioConnector(self._mapper, self._event_source)
        self._game_manager = GameManager(self._event_source, self._gatewayDevice)

    def start(self):
        self._gatewayDevice.start()
        self._connector.start()

 