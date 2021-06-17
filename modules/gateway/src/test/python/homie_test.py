import time

import logging

import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

from homie.device_dimmer import Device_Dimmer
from microsquad.mapper.homie.gateway.device_gateway import Device_Gateway

mqtt_settings = {
    'MQTT_BROKER' : 'localhost',
    'MQTT_PORT' : 1883,
}

# class My_Dimmer(Device_Dimmer):
#     def set_dimmer(self,percent):
#         print('Received MQTT message to set the dimmer to {}. Must replace this method'.format(percent))
#         super().set_dimmer(percent)        

# try:
#     dimmer = My_Dimmer(device_id ='dimmer01', name = 'Test Dimmer',mqtt_settings=mqtt_settings)
#     while True:
#         dimmer.update_dimmer(0)
#         time.sleep(5)
#         dimmer.update_dimmer(50)
#         time.sleep(5)
#         dimmer.update_dimmer(100)
#         time.sleep(5)
# except (KeyboardInterrupt, SystemExit):
#     print("Quitting.")  


try:
    device = Device_Gateway(mqtt_settings=mqtt_settings)
    while True:
        device.update_score("0 - 0")
        device.get_node("player-01").get_property("name").value = "Jose"
        time.sleep(5)
        device.update_score("0 - 1")
        device.get_node("player-01").get_property("name").value = "Lucien"
        time.sleep(5)
        device.update_score("1 - 0")
        device.get_node("player-01").get_property("name").value = "Marcel"
        time.sleep(5)
except (KeyboardInterrupt, SystemExit):
    print("Quitting.")  