import logging

from ..mapper.abstract_mapper import AbstractMapper
from .abstract_connector import AbstractConnector

from rx3 import Observable
from queue import SimpleQueue, Empty

class DummyConnector(AbstractConnector):
    """
    Simple dummy connector implementation that receives messages via a method and queues them up.
    It then forwards the queued message to the mapper (FIFO), when asked to dispatch one.
    """
    def __init__(self, mapper : AbstractMapper, event_source : Observable):
      super().__init__(event_source)
      self._incoming_queue = SimpleQueue()
      self._mapper = mapper
      self.__last_sent = None
      self.__last_sent_device = None
      
    def queue(self, message, device_id = None):
      if device_id is None:
        print("'Sending' Message to Microbits ;-) : {}".format(message))
      else:
        print("'Sending' Message to Microbit Device {} ;-) : {}".format(str(device_id), message))  
        self.__last_sent_device = str(device_id)
      self.__last_sent = message
    
    def simulate_message(self,msg : str):
      """
       Simulate a message coming from one of the microbits
      """
      self._incoming_queue.put(msg)
    
    def dispatch_next(self):
        try:
            next_incoming_message = self._incoming_queue.get_nowait()
            self._mapper.map_from_microbit(next_incoming_message)
        except Empty:
            pass

    @property
    def last_sent(self):
      return self.__last_sent
          

