from microbit import display,radio, sleep

import logging

from ..mapper.abstract_mapper import AbstractMapper
from .abstract_connector import AbstractConnector


class BitioConnector(AbstractConnector):
    """
    Simple Bitio connector implementation that uses the radio to receive messages.
    It also subscribes to a MicroSquadEvent source to queue up messages to the terminals.
    """
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
            # TODO: This call should be asynchronous and delegating to a separate scheduler
            self._mapper.map_from_microbit(incoming_msg)

        if len(self._queue) > 0:
            outgoing_msg = self._queue.pop(0)
            logging.debug("Sending " + outgoing_msg.topic+" "+str(outgoing_msg.payload.decode('ascii')) +" (left "+str(len(self._queue))+")")
            radio.send(str(outgoing_msg.payload.decode('ascii')))
    