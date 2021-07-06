from dotenv import load_dotenv
import time
from homie.device_base import HOMIE_SETTINGS


from microsquad.gateway.mqtt.homie_bitio_gateway import HomieBitioGateway

import rx3

load_dotenv()

MQTT_SETTINGS = {
        'MQTT_BROKER' : 'localhost',
        'MQTT_PORT' : 1883,
        'MQTT_SHARE_CLIENT': True
    }

HOMIE_SETTINGS = {
            "update_interval": 1
        }

event_source = rx3.subject.Subject()
gateway = HomieBitioGateway(HOMIE_SETTINGS, MQTT_SETTINGS, event_source)
gateway.start()

while True:
    time.sleep(50)