from line_protocol_parser import parse_line, LineFormatError

from .gateway.device_gateway import DeviceGateway

import datetime
import logging

from ..abstract_mapper import AbstractMapper

from ...event import EventType,MicroSquadEvent

class HomieMapper(AbstractMapper):
    """
    Homie V4 Mapper - converts incoming MQTT and Microbit radio messages to Homie V4 devices, nodes and properties.
    """
    def __init__(self, gateway: DeviceGateway, event_source) -> None:
        super().__init__(event_source)
        self._gateway = gateway
        

    def map_from_mqtt(self, message):
        """ With a Homie implementation, we are not mapping low-level MQTT messages
            but rather update calls made on properties.
            This is therefore a no-op implementation.
            Instead, we implement a RxPy subscriber, and pass on all command events
            to the connector.
        """
        pass
        

    
    def map_from_microbit(self, message):
        # TODO:  The mapper could become generic and only parse line protocol events
        #        to transform them into reactive events.
        try:
            msg = parse_line(message)
            measurement = msg["measurement"]
            dev_id = msg["fields"]["dev_id"]
            # No-op if the terminal is already known to the gateway
            self._gateway.add_terminal(dev_id)
            # Interpret measurement, Convert fields and tags to Homie device update
            if measurement == "bonjour":
                self.event_source.on_next(MicroSquadEvent(EventType.BONJOUR,dev_id,msg["tags"].copy()))
            elif measurement.startswith("read_"):
                # e.g. "read_button"
                read,verb = measurement.split("_",1)
                
                terminal = self._gateway.terminals[dev_id]
                if verb == "button":
                    # Button A or B ?
                    button_id = "button-"+msg["tags"]["button"]
                    button_node = terminal.get_node(button_id)
                    if(button_node is not None):
                        button_node.get_property("pressed").value=1
                        button_node.get_property("pressed-last").value=datetime.datetime.now().isoformat()
                        button_node.get_property("pressed-count").value=1
                        self.event_source.on_next(MicroSquadEvent(EventType.BUTTON,dev_id,msg["tags"].copy()))
                    else:
                        logging.warn("Button {} is not defined as device node !".format("button_id"))

                    # TODO : Set a timer to reset the pressed state later
                    # Could be easily done with RxPy
                elif verb == "accel":
                    terminal.get_node("accelerator").get_property("x").value=int(msg["tags"]["x"])
                    terminal.get_node("accelerator").get_property("y").value=int(msg["tags"]["y"])
                    terminal.get_node("accelerator").get_property("z").value=int(msg["tags"]["z"])
                    self.event_source.on_next(MicroSquadEvent(EventType.ACCELERATOR,dev_id,msg["tags"].copy()))
                elif verb == "vote":
                    terminal.get_node("vote").get_property("choice-value").value=(msg["tags"]["value"])
                    terminal.get_node("vote").get_property("choice-index").value=int(msg["tags"]["index"])
                    self.event_source.on_next(MicroSquadEvent(EventType.VOTE,dev_id,msg["tags"].copy()))
                elif verb == "temperature":
                    terminal.get_node("temperature").get_property("temperature").value=int(msg["tags"]["value"])
                    self.event_source.on_next(MicroSquadEvent(EventType.TEMPERATURE,dev_id,msg["tags"].copy()))
        except LineFormatError as lfe:
            logging.exception(lfe)
            raise
        except:
             logging.exception("Unexpected error on line message : %s",message)
             raise

