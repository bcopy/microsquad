from abc import ABCMeta,abstractmethod

import logging

from microsquad.mapper.homie.gateway.node_player import NodePlayer

from .abstract_game import AGame, set_next_in_collection, set_prev_in_collection

import enum
import random
from rx3 import Observable
from microsquad.event import EVENTS_SENSOR, EventType, MicroSquadEvent
from microsquad.mapper.homie.gateway.device_gateway import DeviceGateway

from .particles import PARTICLE, PARTICLES


@enum.unique
class TRANSITIONS(enum.Enum):
  START = "Start"
  SEND_PARTICLE1 = "Send first" # Change
  SEND_PARTICLE2 = "Send second" # Change
  SEND_MYSTERY = "Send mystery particle"
  RESEND = "Resend"
  VOTE = "Vote"
  RESULTS = "Show results"
  CLEAR = "Clear"
  def equals(self, string):
       return self.value == string

TRANSITION_GRAPH = { 
                TRANSITIONS.SEND_PARTICLE1 : [TRANSITIONS.SEND_PARTICLE1, TRANSITIONS.SEND_PARTICLE2, TRANSITIONS.SEND_MYSTERY],
                TRANSITIONS.SEND_PARTICLE2 :  [TRANSITIONS.SEND_PARTICLE1, TRANSITIONS.SEND_PARTICLE2, TRANSITIONS.SEND_MYSTERY],
                TRANSITIONS.SEND_MYSTERY : [TRANSITIONS.RESEND,TRANSITIONS.VOTE],
                TRANSITIONS.RESEND : [TRANSITIONS.RESEND,TRANSITIONS.VOTE],
                TRANSITIONS.VOTE : [TRANSITIONS.VOTE,TRANSITIONS.RESULTS],
                TRANSITIONS.RESULTS : [TRANSITIONS.SEND_MYSTERY, TRANSITIONS.CLEAR]
            }

logger = logging.getLogger(__name__)


class AParticleVotingGame(AGame):
    
    def __init__(self, event_source: Observable, gateway : DeviceGateway, particle1:PARTICLE, particle2:PARTICLE, visualizationIndex:int) -> None:
        super().__init__(event_source, gateway)
        self._last_sent_particle = None
        self.PARTICLE1 = particle1
        self.PARTICLE2 = particle2
        self.VISUALIZATION_INDEX = visualizationIndex
        self._votes = {}
        
    def start(self) -> None:
        super().update_available_transitions([TRANSITIONS.SEND_PARTICLE1, TRANSITIONS.SEND_PARTICLE2])

    def process_event(self, event:MicroSquadEvent) -> None:
        logger.debug("Charges received event {} for device {}: {}".format(event.event_type.name, event.device_id, event.payload))
        self.device_gateway.get_node("players-manager").add_player(event.device_id)
        playerNode = self.device_gateway.get_node("player-"+event.device_id)
        say_dur= playerNode.get_property("say-duration").value
        if say_dur is None or say_dur < 300000:
          playerNode.get_property("say-duration").value = 300000
        if event.event_type in EVENTS_SENSOR:
            if super().last_fired_transition == TRANSITIONS.VOTE.value:
                if event.event_type == EventType.VOTE:
                    # Store the player's vote
                    self._votes[event.device_id] = int(event.payload["value"])
                    playerNode.get_property("say").value = "<span>&#127873</span>"
                    

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
        if(last_fired == TRANSITIONS.SEND_PARTICLE1):
            # TODO : Add images and sounds on the scoreboard
            logger.debug("Sending particle "+self.PARTICLE1.identifier)
            
            super().device_gateway.update_broadcast("show,p={},v={}".format(self.PARTICLE1.idx, self.VISUALIZATION_INDEX))
        elif(last_fired == TRANSITIONS.SEND_PARTICLE2):
            # TODO : Add images and sounds on the scoreboard
            logger.debug("Sending particle "+self.PARTICLE2.identifier)
            super().device_gateway.update_broadcast("show,p={},v={}".format(self.PARTICLE2.idx, self.VISUALIZATION_INDEX))
        elif(last_fired == TRANSITIONS.SEND_MYSTERY):
            self._votes = {}
            for pn in self.get_all_player_nodes():
                pn.get_property("animation").value = "Idle"
                pn.get_property("say").value = ""
            self._last_sent_particle = self.get_random_particle()
            logger.debug("Sending {}".format(self._last_sent_particle.identifier))
            super().device_gateway.update_broadcast("show,p={},v={}".format(self._last_sent_particle.idx, self.VISUALIZATION_INDEX))
        elif(last_fired == TRANSITIONS.RESEND):
            logger.debug("Re-Sending {}".format(self._last_sent_particle.identifier))
            super().device_gateway.update_broadcast("show,p={},v={}".format(self._last_sent_particle.idx, self.VISUALIZATION_INDEX))
        elif(last_fired == TRANSITIONS.VOTE):
            super().device_gateway.update_broadcast("vote,v=2")
        elif(last_fired == TRANSITIONS.RESULTS):
            # Tally up the votes, make players say the result, change their animation (DEATH if they are wrong)
            for player_id,vote_value in self._votes.items():
                player_node = self.get_player_node_by_id(player_id)
                if(vote_value == self._last_sent_particle.idx):
                    # Correct vote !
                    player_node.get_property("say").value = "<span>&#9989;</span>"
                    player_node.get_property("animation").value = "Idle"
                else:
                    _defeat(player_node, "&#10060;")
            for player_node in self.get_all_player_nodes():
                if(player_node.get_property("terminal-id").value not in self._votes.keys()):
                    _defeat(player_node, "&#10067;")
        elif(last_fired == TRANSITIONS.CLEAR):
            for player_node in self.get_all_player_nodes():
                player_node.get_property("say").value = ""
                player_node.get_property("animation").value = "Idle"

    def get_random_particle(self) -> PARTICLE:
        return random.choice([self.PARTICLE1, self.PARTICLE2])

    def stop(self) -> None:
        print("{} stopped".format(__name__))


def _defeat(player_node:NodePlayer,emoji_entity:str):
  player_node.get_property("say").value = "<span>{}</span>".format(emoji_entity)
  player_node.get_property("animation").value = "Death"