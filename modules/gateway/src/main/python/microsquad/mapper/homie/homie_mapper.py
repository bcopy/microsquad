from line_protocol_parser import parse_line, LineFormatError

from .gateway.device_gateway import DeviceGateway
from .terminal.device_terminal import DeviceTerminal

import datetime
import logging

from ..abstract_mapper import AbstractMapper


class HomieMapper(AbstractMapper):
    """
    Homie V4 Mapper - converts incoming MQTT messages and outgoing Microbit radio messages to Homie V4 devices, nodes and properties.
    """
    def __init__(self, homie_root_topic, mqtt_settings):
        super.__init__()
        self._homie_root_topic = homie_root_topic

        self._homie_settings = {
            "topic": self._homie_root_topic,
            "update_interval": 1
        }
        self._mqtt_settings = mqtt_settings
        self._gateway = DeviceGateway(homie_settings=self._homie_settings,mqtt_settings=self._mqtt_settings)
        self._terminals = {}
        

    def declare_terminal_if_required(self, device_id):
        if(device_id not in self._terminals.keys()):
            terminal = DeviceTerminal(device_id = "terminal-"+device_id, name="Terminal "+device_id, homie_settings=self._homie_settings, mqtt_settings=self._mqtt_settings)
            terminal.get_node("info").get_property("terminal-id").value = device_id
            terminal.get_node("info").get_property("serial-number").value = device_id
            
            self._terminals[device_id] = terminal
            logging.info("Added new terminal {}".format(device_id))
        else:
            logging.debug("Terminal {} already declared".format(device_id))


    def map_from_mqtt(self, message):
        # Interpret incoming MQTT update and create required devices
        """
        /player-manager/add
        /player/manager/remove
        """
        pass
    
    def map_from_microbit(self, message):
        try:
            msg = parse_line(message)
            measurement = msg.measurement
            dev_id = msg.tags["dev_id"]
            self.declare_terminal_if_required(dev_id)
            # Interpret measurement, Convert fields and tags to Homie device update
            if measurement == "bonjour":
                # TODO : Add BONJOUR event handler callback
                pass
            elif measurement.startswith("read_"):
                # e.g. "read_button_a"
                read,verb,args = "_".split(measurement,2)
                
                terminal = self._terminals[dev_id]
                if verb == "button":
                    # Button A or B ?
                    button_id = "button-"+args
                    terminal.get_node(button_id).get_property("pressed").value=1
                    terminal.get_node(button_id).get_property("pressed-last").value=datetime.datetime.now().isoformat()
                    terminal.get_node(button_id).get_property("pressed-count").value=1

                    # TODO : Set a timer to reset the pressed state later
                elif verb == "accel":
                    terminal.get_node("accelerator").get_property("x").value=int(msg.tags["x"])
                    terminal.get_node("accelerator").get_property("y").value=int(msg.tags["y"])
                    terminal.get_node("accelerator").get_property("z").value=int(msg.tags["z"])
                elif verb == "vote":
                    terminal.get_node("vote").get_property("choice-value").value=(msg.tags["value"])
                    terminal.get_node("vote").get_property("choice-index").value=int(msg.tags["index"])
                elif verb == "temperature":
                    terminal.get_node("temperature").get_property("temperature").value=int(msg.tags["value"])
        except LineFormatError:
            logging.exception("Received invalid line message : %s",message)
        except:
             logging.exception("Unexpected error on line message : %s",message)


