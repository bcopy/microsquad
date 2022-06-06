from rx3 import Observable
from microsquad.game.abstract_game import AGame
from microsquad.mapper.homie.gateway.device_gateway import DeviceGateway
from microsquad.event import MicroSquadEvent

class Game(AGame):
    """ 
    A simple game that allows to declare new players and customize their appearance
    """
    def __init__(self, event_source: Observable, gateway : DeviceGateway) -> None:
        super().__init__(event_source, gateway)
        self.started = False
        self.running = False
        self.stopped = False
        self.received_events : MicroSquadEvent = []
        
    def start(self) -> None:
        print("Test Game starting")
        self.started = True
        self.running = True
        self.available_transitions = ["stop","get_events"]
    
    def process_event(self, event:MicroSquadEvent) -> None:
        """
        Handle the next game event
        """
        if(self.running and self.last_fired_transition == "get_events"):
            self.received_events.append(event)

    def stop(self) -> None:
        print("Test Game stopping")
        self.started = True
        self.running = False
        self.stopped = True
        
