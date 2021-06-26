
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

class MicroSquadEvent():
    def __init__(self, event_type:EventType, payload = None ) -> None:
        self.__event_type = event_type
        self.__payload = payload

    @property
    def event_type(self):
        return self.__event_type

    @property
    def payload(self):
        return self.__payload