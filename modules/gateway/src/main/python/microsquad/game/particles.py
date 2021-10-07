import enum

@enum.unique
class PARTICLE(enum.Enum):
    ELECTRON = ("electron",0)
    PROTON = ("proton",1)
    PHOTON = ("photon", 2)
    NEUTRON = ("neutron",3)
    
    def __init__(self, identifier : str, idx : int) -> None:
        self.idx = idx
        self.identifier = identifier
    

PARTICLES = list(PARTICLE)
