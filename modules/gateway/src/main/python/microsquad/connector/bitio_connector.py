from microbit import display,radio, sleep

import logging

from ..mapper.abstract_mapper import AbstractMapper
from . import AbstractConnector

class BitioConnector(AbstractConnector):
    def __init__(self, mapper : AbstractMapper):
      self._queue = []
      self._mapper = mapper
      radio.config(length=200, channel=12, group=12)
      radio.on()

    def queue(self, message):
        self._queue.append(message)
    
    def dispatch_next(self):
        incoming_msg = radio.receive()
        if incoming_msg != "None":
            # Received message via radio
            logging.debug(incoming_msg)
            # Map the message to logical device
            self._mapper.map_from_microbit(incoming_msg)

        if len(self._queue) > 0:
            outgoing_msg = self._queue.pop(0)

            logging.info("Sending " + outgoing_msg.topic+" "+str(outgoing_msg.payload.decode('ascii')) +" (left "+str(len(self._queue))+")")

            # TODO : Change the radio config to target a particular group of devices ?

            radio.send(str(outgoing_msg.payload.decode('ascii')))
    