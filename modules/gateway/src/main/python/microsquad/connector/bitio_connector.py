from microbit import display,radio, sleep

import logging

from rx3 import Observable

from queue import Queue,Empty

from ..mapper.abstract_mapper import AbstractMapper
from .abstract_connector import AbstractConnector


class BitioConnector(AbstractConnector):
    """
    Simple Bitio connector implementation that uses the radio to receive messages.
    It also subscribes to a MicroSquadEvent source to queue up messages to the terminals.
    """
    def __init__(self, mapper : AbstractMapper, event_source: Observable):
      super().__init__(event_source)
      self._queue = Queue()
      self._mapper = mapper
      radio.config(length=128, channel=12, group=12)
      radio.on()

    def queue(self, message):
        self._queue.put(message)
    
    def dispatch_next(self):
        incoming_msg = radio.receive()
        if incoming_msg != "None" and incoming_msg is not None:
            # Received message via radio
            logging.debug("Receiving "+incoming_msg)
            # Map the message to logical device
            # TODO: This call should be asynchronous and delegating to a separate scheduler
            self._mapper.map_from_microbit(incoming_msg)

        try:
            outgoing_msg = self._queue.get_nowait()
            outgoing_msg_ascii = str(outgoing_msg.decode('ascii'))
            logging.debug("Sending " + outgoing_msg_ascii +" (left "+str(len(self._queue))+")")
            radio.send(outgoing_msg_ascii)
        except Empty:
            pass
    