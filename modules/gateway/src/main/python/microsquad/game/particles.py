import enum

@enum.unique
class PARTICLE(enum.Enum):
    PROTON = ("proton","09990:99399:99999:99990:99000", "30903:30003:30003:30003:30003;30903:30903:30003:30003:30003;30903:30903:30903:39003:90003")
    ELECTRON = ("electron","90009:09090:00000:99999:90909", "30903:30003:30003:30003:30003;30903:30903:30003:30003:30003;30903:30903:30903:30093:30009")

    def __init__(self, identifier : str, display : str, trajectory : str) -> None:
        self.display = display
        self.trajectory = trajectory
        self.identifier = identifier
    

PARTICLES = list(PARTICLE)
