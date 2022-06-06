import logging

from homie.node.property.property_string import Property_String
from homie.node.node_base import Node_Base

from .node_team import NodeTeam

import json

logger = logging.getLogger(__name__)

class NodeTeamManager(Node_Base):

    def __init__(self, device):
      super().__init__(device, id="teams-manager", name="Teams Manager", type_="teams_manager", retain=True, qos=1)
      
      self.add_property(Property_String(self, id="add-player", settable=True, name="add player", set_value = self.add_player ))
      self.add_property(Property_String(self, id="remove-player", settable=True, name="remove player", set_value = self.remove_player ))
      self.add_property(Property_String(self, id="add", settable=True, name="add team", set_value = self.add_team ))
      self.add_property(Property_String(self, id="remove", settable=True, name="remove team", set_value = self.remove_team ))

      self.teams = []
      self.add_property(Property_String(self, id="list", name="list teams" ))
      self.teams_to_players = {}
      self.add_property(Property_String(self, id="list-players", name="list_players" ))

    def refresh_teams_list(self):
        self.get_property("list").value = json.dumps(self.teams, sort_keys=True,separators=(',', ':'))
        self.get_property("list-players").value = json.dumps(self.teams_to_players, sort_keys=True,separators=(',', ':'))

    def add_team(self,team):
        if(not team in self.teams):
            self.device.add_node(NodeTeam(self.device,id="team-"+team, name=team))
            self.teams.append(team)
            if(team not in self.teams_to_players.keys()):
                self.teams_to_players[team] = []
            self.refresh_teams_list()
            logger.info("Team Added : {}".format(team))
        else:
            logger.error("Team {} already exists. Not added.".format(team))

    def remove_team(self,team):
        if(team in self.teams):
            logger.info("Removing team : {}".format(team))
            self.teams.remove(team)
            self.teams_to_players.pop(team)
            self.device.remove_node("team-"+team)
            self.refresh_teams_list()
        else:
            logger.info("Team {} does not exist. Not removed.".format(team))

    def add_player(self,identifier_team_player):
        team,player = identifier_team_player.split(":",1)
        if(team in self.teams):
            logger.info("Adding Player {} to Team {}".format(player,team))
            if(player not in self.teams_to_players[team]):
                self.teams_to_players[team].append(player)
                self.refresh_team_node(team)
                self.refresh_teams_list()
                logger.debug("Added Player {} to Team {}".format(player,team))
            else:
              logger.debug("Player {} is already in Team {} !".format(player,team))
        else:
            logger.info("Team {} does not exist. Not adding player {}.".format(team, player))
    
    def remove_player(self,identifier_team_player):
        team,player = identifier_team_player.split(":",1)
        if(team in self.teams):
            logger.info("Removing Player {} from Team {}".format(player,team))
            if(team in self.teams_to_players.keys()):
                if(player in self.teams_to_players[team]):
                    self.teams_to_players[team].remove(player)
                    self.refresh_teams_list()
                    logger.debug("Removed Player {} from Team {}".format(player,team))
        else:
            logger.info("Team {} does not exist. Not removing player {}.".format(team, player))

    def refresh_team_node(self,team_to_refresh):
        players_list = self.teams_to_players[team_to_refresh]
        self.device.get_node("team-"+team_to_refresh).get_property("players").value = ",".join(players_list)



        

