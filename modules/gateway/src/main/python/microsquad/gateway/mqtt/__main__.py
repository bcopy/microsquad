from dotenv import load_dotenv
import time
import argparse
import logging
from homie.device_base import HOMIE_SETTINGS


from .homie_bitio_gateway import HomieBitioGateway

import rx3

load_dotenv()

logging.basicConfig(encoding='ascii', level=logging.INFO)
logging.getLogger('homie').setLevel(logging.WARN)

MQTT_SETTINGS = {
        'MQTT_BROKER' : 'localhost',
        'MQTT_PORT' : 1883,
        'MQTT_SHARE_CLIENT': True
    }

HOMIE_SETTINGS = {
            "update_interval": 1,
            "topic": "microsquad"
        }

# parser = argparse.ArgumentParser(description='Run a MicroSquad gateway.')
# parser.add_argument('-t','--test', action='store_true',
#                     help='Run the gateway in interactive mode without a Microbit connector')
# parser.add_argument('--connector', type=ascii, default="bitio", choices=["dummy","bitio"],
#                     help='Specify the connector you are using')

# args = parser.parse_args()


event_source = rx3.subject.Subject()

gateway = HomieBitioGateway(HOMIE_SETTINGS, MQTT_SETTINGS, event_source)
gateway.start()

while True:
    time.sleep(5)