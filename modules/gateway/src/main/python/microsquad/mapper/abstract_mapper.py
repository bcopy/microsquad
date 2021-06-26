from abc import ABCMeta,abstractmethod

import logging

class AbstractMapper(metaclass=ABCMeta):
 
    @abstractmethod
    def map_from_mqtt(self, message):
        pass
    
    @abstractmethod
    def map_from_microbit(self, message):
        pass
