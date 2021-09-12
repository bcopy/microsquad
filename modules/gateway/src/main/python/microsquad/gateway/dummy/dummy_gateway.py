
import logging

from rx3 import Observable
from rx3.subject import Subject

from ...mapper.homie.gateway.device_gateway import DeviceGateway
from ...mapper.homie.homie_mapper import HomieMapper
from ...connector.dummy_connector import DummyConnector

gateway = None

class HomieDummyGateway:
    

    """
    MicroSquad Gateway Dummy Homie implementation.
    The Dummy implementation does not actually connect to Microbit terminals. It is used primarily for interactive testing.
    """
    def __init__(self, homie_settings, mqtt_settings, event_source: Observable):
        
        self._event_source = event_source
        self._homie_settings = homie_settings
        self._mqtt_settings = mqtt_settings
        self.deviceGateway = DeviceGateway(event_source = self._event_source, homie_settings=self._homie_settings,mqtt_settings=self._mqtt_settings)
        self.mapper = HomieMapper(self.deviceGateway, self._event_source)
        self.connector = DummyConnector(self.mapper)

    def start(self):
        self.deviceGateway.start()
        self.connector.start()

    

def main():
    global gateway
    MQTT_SETTINGS = {
            'MQTT_BROKER' : 'localhost',
            'MQTT_PORT' : 1883,
            'MQTT_SHARE_CLIENT': True
        }

    HOMIE_SETTINGS = {
                "update_interval": 1
            }

    event_source = Subject()

    gateway = HomieDummyGateway(HOMIE_SETTINGS, MQTT_SETTINGS, event_source)
    print("Starting dummy gateway...")
    gateway.start()


if __name__ == "__main__":
    main()