from microsquad.game.particle_voting_game import AParticleVotingGame
import base64
import random
from rx3 import Observable
from microsquad.mapper.homie.gateway.device_gateway import DeviceGateway

from ..particles import PARTICLE, PARTICLES

class Game(AParticleVotingGame):
    def __init__(self, event_source: Observable, gateway : DeviceGateway) -> None:
        super().__init__(event_source, gateway, PARTICLE.ELECTRON, PARTICLE.POSITRON, 2)
        with open("src/main/python/microsquad/game/antimatter-summary.png", "rb") as image_file:
            string_data = base64.b64encode(image_file.read())
            super().device_gateway.get_node("scoreboard").get_property("image").value = "data:image/png;base64,"+(string_data.decode("ascii"))


    def get_random_particle(self):
        return random.choice([PARTICLE.ELECTRON,PARTICLE.POSITRON])
        