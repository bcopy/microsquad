from microbit import display,radio, sleep

import logging
from . import AbstractConnector

class BitioConnector(AbstractConnector):
    def __init__(self, mapper):
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

            # Find out which device to send the message to ...

            # 

            logging.info("Sending " + outgoing_msg.topic+" "+str(outgoing_msg.payload.decode('ascii')) +" (left "+str(len(self._queue))+")")

            # Instead of broadcast, may need to send to only one device
            radio.send(str(outgoing_msg.payload.decode('ascii')))
    