from rx3 import Observable
from microsquad.event import EventType, MicroSquadEvent
from microsquad.mapper.homie.gateway.device_gateway import DeviceGateway
import enum
import logging

from ..abstract_game import AGame, set_next_in_collection, set_prev_in_collection

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

ATTITUDES = ["Idle","Run","Walk","CrouchWalk","Wave"]



@enum.unique
class TRANSITIONS(enum.Enum):
  SELECT_SKIN = "Select skin"
  SELECT_ATTITUDE = "Select attitude"
  EMOJIS = "Emojis"

TRANSITION_GRAPH = { 
                TRANSITIONS.SELECT_SKIN : [TRANSITIONS.SELECT_ATTITUDE],
                TRANSITIONS.SELECT_ATTITUDE : [TRANSITIONS.EMOJIS],
                TRANSITIONS.EMOJIS : [TRANSITIONS.EMOJIS]
            }

logger = logging.getLogger(__name__)

class Game(AGame):
    """ 
    A simple game that allows to declare new players and customize their appearance
    """
    def __init__(self, event_source: Observable, gateway : DeviceGateway) -> None:
        super().__init__(event_source, gateway)
        
    def start(self) -> None:
        print("Customeeze starting")
        super().update_available_transitions([TRANSITIONS.SELECT_SKIN])
        super().device_gateway.update_broadcast("buttons")

    def process_event(self, event:MicroSquadEvent) -> None:
        logger.debug("Customeeze received event {} for device {}: {}".format(event.event_type.name, event.device_id, event.payload))
        self.device_gateway.get_node("players-manager").add_player(event.device_id)
        if event.event_type==EventType.BUTTON:
            playerNode = self.device_gateway.get_node("player-"+event.device_id)
            if playerNode is None:
                logger.warn("Player {} is not known".format("player-"+event.device_id))
            else:
                if super().last_fired_transition is None or super().last_fired_transition not in [TRANSITIONS.SELECT_ATTITUDE.value, TRANSITIONS.SELECT_SKIN.value]:
                    playerNode.get_property("animation").value = "Wave"
                elif super().last_fired_transition == TRANSITIONS.SELECT_SKIN.value:
                    if event.payload["button"]=="a" :
                        # Shift the player's skin
                        set_next_in_collection(playerNode.get_property("skin"), SKINS)
                    elif event.payload["button"]=="b" :
                        # Shift the player's skin
                        set_prev_in_collection(playerNode.get_property("skin"), SKINS)
                elif super().last_fired_transition == TRANSITIONS.SELECT_ATTITUDE.value:
                    if event.payload["button"]=="a" :
                        set_next_in_collection(playerNode.get_property("animation"), ATTITUDES)
                    elif event.payload["button"]=="b" :
                        set_prev_in_collection(playerNode.get_property("animation"), ATTITUDES)
                    
                elif super().last_fired_transition == TRANSITIONS.EMOJIS.value:
                    # if event.payload["button"]=="a" :
                    #     # Shift the player's attitude
                    #     set_next_in_collection(playerNode.get_property("skin"), SKINS)
                    # elif event.payload["button"]=="b" :
                    #     # Shift the player's attitude
                    #     set_prev_in_collection(playerNode.get_property("skin"), SKINS)
                    pass
                    

    def fire_transition(self, transition) -> None:
        super().fire_transition(transition)
        # Obtain the next transitions in the graph
        # If none, the game can be stopped
        next_transitions = None
        try:
          next_transitions = TRANSITION_GRAPH[TRANSITIONS(self._last_fired_transition)]
          
        except KeyError:
          logger.debug("No next transitions available after "+self._last_fired_transition)
        
        if(next_transitions is not None and len(next_transitions) > 0):
                super().update_available_transitions(next_transitions)
        else:
                super().update_available_transitions([])  
        
        if(TRANSITIONS(self._last_fired_transition) == TRANSITIONS.EMOJIS):
              # Switch everybody back to idle
              # Trigger a vote
            #   super().device_gateway.update_broadcast("vote,value=90009:09090:00000:99999:90909;09990:99399:99999:99990:99000;90900:90900:99990:99399:99999;09900:99390:99999:00099:99990,duration=4000,votes=4")
            super().device_gateway.update_broadcast("vote_particles") 


    def stop(self) -> None:
        print("Customeeze stopped")

