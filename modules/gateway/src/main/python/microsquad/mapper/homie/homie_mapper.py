from ..line_protocol_parser import LineProtocolParser
from rx3 import Observable

from .gateway.device_gateway import DeviceGateway

import datetime
import logging

from ..abstract_mapper import AbstractMapper

from ...event import EventType,MicroSquadEvent

logger = logging.getLogger(__name__)

def _add_properties_to_tags(node, properties, tags) -> None:
    for prop in properties:
        tags[prop] = node.get_property(prop).value
    
class HomieMapper(AbstractMapper):
    """
    Homie V4 Mapper - converts incoming MQTT and Microbit radio messages to Homie V4 devices, nodes and properties.
    """
    def __init__(self, gateway: DeviceGateway, event_source: Observable) -> None:
        super().__init__(event_source)
        self._gateway = gateway
        self._parser = LineProtocolParser()
        

    def map_from_mqtt(self, message):
        """ With a Homie implementation, we are not mapping low-level MQTT messages
            but rather update calls made on properties.
            This is therefore a no-op implementation.
            Instead, we implement a RxPy observable, and pass on all command events
            to the connector.
        """
        pass
        

    
    def map_from_microbit(self, message):
        # TODO:  The mapper could become generic and only parse line protocol events
        #        to transform them into reactive events.
        try:
            # logger.debug(">> Raw message '" + message+"'")
            msg = self._parser.parse(message)
            measurement = msg[0]
            tags = msg[1]
            dev_id = tags["dev_id"]

            # This is No-op if the terminal is already known to the gateway
            self._gateway.add_terminal(dev_id)

            # Interpret measurement, Convert fields and tags to Homie device update
            if measurement == EventType.BONJOUR.value:
                self.event_source.on_next(MicroSquadEvent(EventType.BONJOUR,dev_id,tags.copy()))
            elif measurement.startswith("read_"):
                # e.g. "read_button"
                read,verb = measurement.split("_",1)
                
                terminal = self._gateway.terminals[dev_id]
                if verb == EventType.BUTTON.value:
                    # Button A or B ?
                    button_id = "button-"+tags["button"]
                    button_node = terminal.get_node(button_id)
                    if(button_node is not None):
                        button_node.get_property("pressed").value=1
                        button_node.get_property("last").value=datetime.datetime.now().isoformat()
                        button_node.get_property("count").value +=1
                        _add_properties_to_tags(button_node,["pressed","last", "count"],tags)
                        self.event_source.on_next(MicroSquadEvent(EventType.BUTTON,dev_id,tags.copy()))
                    else:
                        logging.warn("Button {} is not defined as device node !".format("button_id"))

                    # TODO : Set a timer to reset the pressed state later
                    # Could be easily done with RxPy
                elif verb == EventType.ACCELERATOR.value:
                    accel_node = terminal.get_node("accel")
                    accel_node.get_property("x").value=int(tags["x"])
                    accel_node.get_property("y").value=int(tags["y"])
                    accel_node.get_property("z").value=int(tags["z"])
                    accel_node.get_property("value").value="{x},{y},{z}".format(**tags)
                    _add_properties_to_tags(accel_node,["value"],tags)
                    self.event_source.on_next(MicroSquadEvent(EventType.ACCELERATOR,dev_id,tags.copy()))
                elif verb == EventType.VOTE.value:
                    vote_node = terminal.get_node("vote")
                    vote_node.get_property("value").value=(tags["value"])
                    vote_node.get_property("index").value=int(tags["index"])
                    vote_node.get_property("last").value=datetime.datetime.now().isoformat()
                    _add_properties_to_tags(vote_node,["last"],tags)
                    self.event_source.on_next(MicroSquadEvent(EventType.VOTE,dev_id,tags.copy()))
                elif verb == EventType.TEMPERATURE.value:
                    terminal.get_node("temperature").get_property("temperature").value=int(tags["value"])
                    self.event_source.on_next(MicroSquadEvent(EventType.TEMPERATURE,dev_id,tags.copy()))
        except:
             logging.exception("Unexpected error on line message : %s",message)
             raise

