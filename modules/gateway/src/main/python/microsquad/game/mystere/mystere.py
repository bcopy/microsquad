import logging

from microsquad.mapper.homie.gateway.node_player import NodePlayer
from microsquad.mapper.homie.terminal.device_terminal import DeviceTerminal

from ..abstract_game import AGame, set_next_in_collection, set_prev_in_collection

import enum
import random
from rx3 import Observable
from microsquad.event import EVENTS_SENSOR, EventType, MicroSquadEvent
from microsquad.mapper.homie.gateway.device_gateway import DeviceGateway

from ..particles import PARTICLE, PARTICLES


@enum.unique
class TRANSITIONS(enum.Enum):
  START = "Start"
  SEND_PARTICLE = "Send particle"
  RESEND = "Resend"
  VOTE = "Vote"
  RESULTS = "Show results"
  END = "End Game"
  CLEAR = "Clear"
  RESET = "Reset"
  def equals(self, string):
       return self.value == string

TRANSITION_GRAPH = { 
                TRANSITIONS.START : [TRANSITIONS.START,TRANSITIONS.SEND_PARTICLE],
                TRANSITIONS.SEND_PARTICLE : [TRANSITIONS.RESEND,TRANSITIONS.VOTE],
                TRANSITIONS.RESEND : [TRANSITIONS.RESEND,TRANSITIONS.VOTE],
                TRANSITIONS.VOTE : [TRANSITIONS.VOTE,TRANSITIONS.RESULTS],
                TRANSITIONS.RESULTS : [TRANSITIONS.SEND_PARTICLE, TRANSITIONS.END],
                TRANSITIONS.END : [TRANSITIONS.RESET,TRANSITIONS.CLEAR]
            }

logger = logging.getLogger(__name__)


class Game(AGame):
    def __init__(self, event_source: Observable, gateway : DeviceGateway) -> None:
        super().__init__(event_source, gateway)
        self._last_sent_particle = None
        self._votes = {}
        self._scores = {}
        
    def start(self) -> None:
        print("Mystery Particles game starting")
        super().update_available_transitions([TRANSITIONS.SEND_PARTICLE])
        self.fire_transition(TRANSITIONS.START)

    def process_event(self, event:MicroSquadEvent) -> None:
        logger.debug("Game received event {} for device {}: {}".format(event.event_type.name, event.device_id, event.payload))
        self.device_gateway.get_node("players-manager").add_player(event.device_id)
        playerNode = self.device_gateway.get_node("player-"+event.device_id)
        say_dur= playerNode.get_property("say-duration").value
        if say_dur is None or say_dur < 300000:
          playerNode.get_property("say-duration").value = 300000
        if event.event_type in EVENTS_SENSOR:
            if self._last_fired_transition == TRANSITIONS.START.value:
                if event.event_type == EventType.BUTTON:
                    playerNode.get_property("animation").value = "Wave"
            if self._last_fired_transition == TRANSITIONS.VOTE.value:
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
        if(last_fired == TRANSITIONS.START):
            super().device_gateway.update_broadcast("buttons")
        elif(last_fired == TRANSITIONS.SEND_PARTICLE):
            self._votes = {}
            for player_node in self.get_all_player_nodes():
                player_node.get_property("animation").value = "Idle"
                player_node.get_property("say").value = ""
            self._last_sent_particle = random.choice(PARTICLES)
            logger.debug("Sending {}".format(self._last_sent_particle.identifier))
            
            # Split the detectors into three categories, send them different visualizations
            self._dispatch_visualizations(self._last_sent_particle)

        elif(last_fired == TRANSITIONS.RESEND):
            logger.debug("Re-Sending {}".format(self._last_sent_particle.identifier))
            self._dispatch_visualizations(self._last_sent_particle)
        elif(last_fired == TRANSITIONS.VOTE):
            super().device_gateway.update_broadcast("vote,v=3")
        elif(last_fired == TRANSITIONS.RESULTS):
            # Tally up the votes, make players say the result, change their animation (DEATH if they are wrong)
            for player_id,vote_value in self._votes.items():
                player_node = self.get_player_node_by_id(player_id)
                if(vote_value == self._last_sent_particle.idx):
                    # Correct vote !
                    player_node.get_property("say").value = "<span>&#9989;</span>"
                    player_node.get_property("animation").value = "Idle"
                    player_node.get_property("scale").value *= 1.1
                    if player_id not in self._scores.keys():
                        self._scores[player_id] = 0
                    self._scores[player_id] += 1
                else:
                    _defeat(player_node, "&#10060;")
            for player_node in self.get_all_player_nodes():
                if(player_node.get_property("terminal-id").value not in self._votes.keys()):
                    _defeat(player_node, "&#10067;")
        elif(last_fired == TRANSITIONS.CLEAR):
            for player_node in self.get_all_player_nodes():
                player_node.get_property("say").value = ""
                player_node.get_property("animation").value = "Idle"
        elif(last_fired == TRANSITIONS.RESET):
            for player_node in self.get_all_player_nodes():
                player_node.get_property("say").value = ""
                player_node.get_property("animation").value = "Idle"
                player_node.get_property("scale").value = 1.0

    def _dispatch_visualizations(self,sent_particle:PARTICLE):
        for index,player_node in enumerate(super().get_all_player_nodes()):
            terminal_id = player_node.get_property("terminal-id").value
            terminal_node: DeviceTerminal = super().device_gateway.terminals[terminal_id]
            terminal_node.update_command("show,p={},v={}".format(sent_particle.idx,index%3))

    def stop(self) -> None:
        print("Mystere stopped")


def _defeat(player_node:NodePlayer,emoji_entity:str):
  player_node.get_property("say").value = "<span>{}</span>".format(emoji_entity)
  player_node.get_property("animation").value = "Death"
  player_node.get_property("scale").value *= 0.9