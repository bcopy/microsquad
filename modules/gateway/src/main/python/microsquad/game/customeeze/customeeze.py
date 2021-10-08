from rx3 import Observable
from microsquad.event import EVENTS_SENSOR, EventType, MicroSquadEvent
from microsquad.mapper.homie.gateway.device_gateway import DeviceGateway
import enum
import logging

from ..abstract_game import AGame, set_next_in_collection, set_prev_in_collection, find_emote_by_idx

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
  CLEAR = "Clear"
  def equals(self, string):
       return self.value == string

TRANSITION_GRAPH = { 
                TRANSITIONS.SELECT_SKIN : [TRANSITIONS.SELECT_ATTITUDE],
                TRANSITIONS.SELECT_ATTITUDE : [TRANSITIONS.EMOJIS],
                TRANSITIONS.EMOJIS : [TRANSITIONS.EMOJIS, TRANSITIONS.CLEAR]
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
        if event.event_type in EVENTS_SENSOR:
            playerNode = self.device_gateway.get_node("player-"+event.device_id)
            if playerNode is None:
                logger.warn("Player {} is not known".format("player-"+event.device_id))
            else:
                if super().last_fired_transition is None:
                    playerNode.get_property("animation").value = "Wave"
                else:
                    last_fired = TRANSITIONS(super().last_fired_transition)
                    if last_fired == TRANSITIONS.SELECT_SKIN:
                        if event.payload["button"]=="a" :
                            # Shift the player's skin
                            set_next_in_collection(playerNode.get_property("skin"), SKINS)
                        elif event.payload["button"]=="b" :
                            # Shift the player's skin
                            set_prev_in_collection(playerNode.get_property("skin"), SKINS)
                    elif last_fired == TRANSITIONS.SELECT_ATTITUDE:
                        if event.payload["button"]=="a" :
                            set_next_in_collection(playerNode.get_property("animation"), ATTITUDES)
                        elif event.payload["button"]=="b" :
                            set_prev_in_collection(playerNode.get_property("animation"), ATTITUDES)
                    elif last_fired == TRANSITIONS.EMOJIS:
                        if event.event_type == EventType.VOTE:
                            emote = find_emote_by_idx(int(event.payload["value"]))
                            if emote is not None:
                                playerNode.get_property("say").value = "<span>{} !</span>".format(emote.entity)
                    

                    

    def fire_transition(self, transition) -> None:
        super().fire_transition(transition)
        # Obtain the next transitions in the graph
        # If none, the game can be stopped
        next_transitions = TRANSITION_GRAPH.get(TRANSITIONS(self._last_fired_transition), None)
        
        if(next_transitions is not None and len(next_transitions) > 0):
                super().update_available_transitions(next_transitions)
        else:
                super().update_available_transitions([])  
        
        last_fired = TRANSITIONS(self._last_fired_transition)
        if( last_fired == TRANSITIONS.EMOJIS):
              # Switch everybody back to idle
              # Trigger a vote
            super().device_gateway.update_broadcast("emote,v=5") 
        elif(last_fired == TRANSITIONS.CLEAR):
            for pn in self.get_all_player_nodes():
                pn.get_property("say-duration").value = 60000
                pn.get_property("say").value = ""
                pn.get_property("animation").value = ""


    def stop(self) -> None:
        print("Customeeze stopped")

