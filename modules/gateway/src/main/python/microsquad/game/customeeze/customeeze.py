from homie.node.property.property_base import Property_Base
from rx3 import Observable
from microsquad.event import EventType, MicroSquadEvent
from microsquad.mapper.homie.gateway.device_gateway import DeviceGateway

import logging

from ..abstract_game import AGame

SKINS = [
        "alienA","alienB","animalA","animalB","animalBaseA","animalBaseB","animalBaseC","animalBaseD","animalBaseE","animalBaseF"
        ,"animalBaseG","animalBaseH","animalBaseI","animalBaseJ","animalC","animalD","animalE","animalF","animalG","animalH","animalI"
        ,"animalJ","astroFemaleA","astroFemaleB","astroMaleA","astroMaleB"
        ,"athleteFemaleBlue","athleteFemaleGreen","athleteFemaleRed","athleteFemaleYellow","athleteMaleBlue","athleteMaleGreen"
        ,"athleteMaleRed","athleteMaleYellow"
        ,"businessMaleA","businessMaleB"
        ,"casualFemaleA","casualFemaleB","casualMaleA","casualMaleB","cyborg"
        ,"fantasyFemaleA","fantasyFemaleB","fantasyMaleA","fantasyMaleB","farmerA","farmerB"
        ,"militaryFemaleA","militaryFemaleB","militaryMaleA","militaryMaleB"
        ,"racerBlueFemale","racerBlueMale","racerGreenFemale","racerGreenMale","racerOrangeFemale","racerOrangeMale"
        ,"racerPurpleFemale","racerPurpleMale","racerRedFemale","racerRedMale","robot","robot2","robot3"
        ,"survivorFemaleA","survivorFemaleB","survivorMaleA","survivorMaleB","zombieA","zombieB","zombieC"
]

ATTITUDES = ["Idle","Run","Walk","CrouchWalk"]

logger = logging.getLogger(__name__)

def _set_next_in_collection(property: Property_Base, collection) -> None:
    idx = 0
    current_value = property.value
    if(current_value in collection):
        idx = collection.index(current_value) +1
    if(idx >= len(collection)) :
        idx = 0
    property.value = collection[idx]


class Game(AGame):
    """ 
    A simple game that allows to declare new players and customize their appearance
    """
    def __init__(self, event_source: Observable, gateway : DeviceGateway) -> None:
        super().__init__(event_source, gateway)
        
    def start(self) -> None:
        print("Customeeze starting")

    def process_event(self, event:MicroSquadEvent) -> None:
        logger.debug("Customeeze received event {} for device {}: {}".format(event.event_type.name, event.device_id, event.payload))
        self.device_gateway.get_node("players-manager").add_player(event.device_id)
        if event.event_type==EventType.BUTTON:
            playerNode = self.device_gateway.get_node("player-"+event.device_id)
            if playerNode is None:
                logger.warn("Player {} is not known".format("player-"+event.device_id))
            else:
                if event.payload["button"]=="a" :
                    # Shift the player's skin
                    _set_next_in_collection(playerNode.get_property("skin"), SKINS)
                elif event.payload["button"]=="b" :
                    # Shift the player's skin
                    _set_next_in_collection(playerNode.get_property("animation"), ATTITUDES)

    def stop(self) -> None:
        print("Customeeze stopped")

