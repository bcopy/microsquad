
import enum

@enum.unique
class EventType(enum.Enum):
    BONJOUR = "bonjour"
    VOTE = "vote"
    ACCELERATOR = "accel"
    BUTTON = "button"
    TEMPERATURE = "temperature"
    TERMINAL_BROADCAST = "terminal_broadcast"
    TERMINAL_COMMAND = "terminal_command"
    TERMINAL_DISCOVERED = "terminal_discovered"
    GAME_DISCOVERED = "game_discovered"
    PLAYER_DISCOVERED = "player_discovered"
    
    def equals(self, string):
       return self.value == string

class MicroSquadEvent():
    def __init__(self, event_type:EventType, device_id=None, payload = None ) -> None:
        self.__event_type = event_type
        self.__payload = payload
        self.__device_id = device_id

    @property
    def event_type(self):
        return self.__event_type

    @property
    def payload(self):
        return self.__payload

    @property
    def device_id(self):
        return self.__device_id