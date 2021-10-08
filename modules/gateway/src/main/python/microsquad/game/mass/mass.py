from microsquad.game.particle_voting_game import AParticleVotingGame

import random
from rx3 import Observable
from microsquad.mapper.homie.gateway.device_gateway import DeviceGateway

from ..particles import PARTICLE, PARTICLES

class Game(AParticleVotingGame):
    def __init__(self, event_source: Observable, gateway : DeviceGateway) -> None:
        super().__init__(event_source, gateway, PARTICLE.PHOTON, PARTICLE.NEUTRON, 1)
        