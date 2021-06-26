from abc import ABCMeta,abstractmethod

from rx3 import Observable

class AbstractMapper(metaclass=ABCMeta):
    """
    Maps communication events between terminals and MQTT.
    Events are propagated using an RxPy event source.
    """
    def __init__(self, event_source) -> None:
        self._event_source = event_source
 
    @property
    def event_source(self) -> Observable:
        return self._event_source

    @abstractmethod
    def map_from_mqtt(self, message):
        pass
    
    @abstractmethod
    def map_from_microbit(self, message):
        pass

    

    

    