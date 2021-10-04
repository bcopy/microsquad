from abc import ABCMeta,abstractmethod

import logging
import threading
from microsquad.event import EventType, MicroSquadEvent

from rx3 import Observable
from rx3.operators import filter

logger = logging.getLogger(__name__)

class AbstractConnector(metaclass=ABCMeta):
    """
    Thread-based implementation of a connector loop.
    """

    @abstractmethod
    def queue(self, message, device_id = None):
        """
        Queue a message for radio distribution
        """
        pass
    
    @abstractmethod
    def dispatch_next(self):
        pass

    def __init__(self, event_source: Observable):
        self._thread_terminate = True
        self._event_source = event_source
        self._event_source.pipe(
            filter(lambda e: e.event_type in [EventType.TERMINAL_BROADCAST, EventType.TERMINAL_COMMAND] )
        ).subscribe(
            on_next = lambda evt: self.queue(evt.payload, evt.device_id)
        )
        
    def start(self):
        self._thread_terminate = False
        self._thread = threading.Thread(target=self._thread_main)
        self._thread.daemon = True
        self._thread.start()

    def _thread_main(self):
        run = True
        error_count = 0

        while run:
            try: 
              self.dispatch_next()
            except:
                error_count += 1
                logging.exception("Error during connector dispatch")
                if error_count > 10:
                    logging.fatal("Error count exceeded, exiting connector loop")
                    self._thread_terminate = True
                
            def should_exit():
                return run is False or self._thread_terminate is True

            if should_exit():
                run = False