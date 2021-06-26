from abc import ABCMeta,abstractmethod

from rx3 import Observable
from rx3.operators import of,map,filter

class AbstractMapper(metaclass=ABCMeta):
    """
    Maps communication events between terminals and MQTT.
    """

    def __init__(self) -> None:
        self.event_source = Observable.create()
 
    def get_event_source(self) -> Observable:
        return self.event_source

    @abstractmethod
    def map_from_mqtt(self, message):
        pass
    
    @abstractmethod
    def map_from_microbit(self, message):
        pass

    def subscribe(self, observer) -> None:
        """
        Subscribe an RxPy observer (it must implement on_next() and can implement
        error and completion handlers)

        :param observer: An RxPy observer handling mapping events 
        """
        self.event_source.subscribe(observer)
    

    

    