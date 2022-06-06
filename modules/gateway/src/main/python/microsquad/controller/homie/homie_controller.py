
import logging
from homieclient import HomieClient

from rx3 import Observable

from ...event import MicroSquadEvent,EventType

logger = logging.getLogger(__name__)


class HomieController():


    """
    A controller that relies on homieclient to obtain and cache property updates, as well
    as issue callbacks on discovery events.
    """
    def __init__(self,mqtt_settings,homie_settings, event_source : Observable = None) -> None:
        self.mqtt_settings = mqtt_settings
        self.homie_settings = {"HOMIE_PREFIX":"homie/"}
        self.homie_settings.update(homie_settings)
        self.homie_client = None
        self.mqtt_transport = "tcp"
        self.event_source = event_source
        self._known_terminals = []
        self._known_games = []
        self._known_players = []


    def connect(self):
        logger.debug(
            "MQTT Connecting to {} as client {}".format(
                self.mqtt_settings["MQTT_BROKER"], self.mqtt_settings["MQTT_CLIENT_ID"]
            )
        )
        """
        HomieClient limitations :
          * No Websockets support (WS_PATH, MQTT_TRANSPORT, TLS SUPPORT)
          * Read-only : does not support updating properties
          * Does not use asyncio futures
        """
        self.homie_client = HomieClient(server=self.mqtt_settings["MQTT_BROKER"], prefix=self.homie_settings["HOMIE_PREFIX"])
        self.homie_client._on_property_updated = self._on_property_updated

        self.homie_client.connect()

    def property_updated(self,node, property, value:str):
        # Check if it's a terminal device
        # If so, issue callbacks and rxpy events
        if(node.device.id.startswith("terminal-") and node.device.id not in self._known_terminals):
            self._known_terminals.append(node.device.id)
            # Terminal event
            if(self.event_source is not None):
                logger.debug(f"New terminal detected : {node.device['device-id']}")
                self.event_source.on_next(MicroSquadEvent(EventType.TERMINAL_DISCOVERED,node.device["device-id"]))
                # Forward the event to any RxPy observers
                self.event_source.on_next(MicroSquadEvent(EventType[str(node.name+"_"+property)],node.device["device-id"],value))

        if(node.name.startswith("game") ):
            if(property == "audience-code" and value not in self._known_games):
                self._known_games.append(value)
                # Terminal event
                if(self.event_source is not None):
                    logger.debug(f"New game started : {value}")
                    self.event_source.on_next(MicroSquadEvent(EventType.GAME_DISCOVERED,payload=value))
                    # TODO : Reset all known players ? all known terminals ?
            # TODO: Forward the property update to any listeners

        if(node.name.startswith("player-") ):
            if(property == "terminal-id" and value not in self._known_players):
                self._known_games.append(value)
                if(self.event_source is not None):
                    logger.debug(f"New player discovered : {value}")
                    self.event_source.on_next(MicroSquadEvent(EventType.PLAYER_DISCOVERED,payload=value))
            # TODO: Forward the property update to any listeners
            
