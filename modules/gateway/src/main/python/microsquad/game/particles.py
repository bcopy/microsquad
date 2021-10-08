import enum

@enum.unique
class PARTICLE(enum.Enum):
    ELECTRON = ("electron",0)
    PROTON = ("proton",1)
    PHOTON = ("photon", 2)
    NEUTRON = ("neutron",3)
    POSITRON = ("positron",4)
    ANTIPROTON = ("antiproton",5)
    
    def __init__(self, identifier : str, idx : int) -> None:
        self.idx = idx
        self.identifier = identifier
    

PARTICLES = list(PARTICLE)

def find_emote_by_idx(idx:int) -> PARTICLE:
    return next((p for p in list(PARTICLE) if p.idx == idx), None)

def find_emote_by_ide(id:str) -> PARTICLE:
    return next((p for p in list(PARTICLE) if p.identifier == id), None)
