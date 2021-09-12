from dotenv import load_dotenv
import time
import argparse
from homie.device_base import HOMIE_SETTINGS


from .homie_bitio_gateway import HomieBitioGateway

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

# parser = argparse.ArgumentParser(description='Run a MicroSquad gateway.')
# parser.add_argument('-t','--test', action='store_true',
#                     help='Run the gateway in interactive mode without a Microbit connector')
# parser.add_argument('--connector', type=ascii, default="bitio", choices=["dummy","bitio"],
#                     help='Specify the connector you are using')

# args = parser.parse_args()


event_source = rx3.subject.Subject()

# if args.connector == "dummy" or args.test == 1:
#   gateway = HomieDummyGateway(HOMIE_SETTINGS, MQTT_SETTINGS, event_source)
# # elif args.connector == "bitio":
gateway = HomieBitioGateway(HOMIE_SETTINGS, MQTT_SETTINGS, event_source)
gateway.start()

while True:
    time.sleep(50)