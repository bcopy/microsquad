
import enum

@enum.unique
class MappingEventType(enum.Enum):
    BONJOUR = "bonjour"
    VOTE = "vote"
    ACCELERATOR = "accel"
    BUTTON = "button"
    TEMPERATURE = "temperature"

class MappingEvent():
    def __init__(self, event_type:MappingEventType, payload = None ) -> None:
        self.__event_type = event_type
        self.__payload = payload

    @property
    def event_type(self):
        return self.__event_type

    @property
    def payload(self):
        return self.__payload