import enum

@enum.unique
class EMOTE(enum.Enum):
    HEART = ("heart",0, "&#10084;")
    SAD = ("sad",1, "&#128542;")
    HAPPY = ("happy",2, "&#128512;")
    SKULL = ("skull",3, "&#128565;")

    def __init__(self, id:str,idx:int, entity:str) -> None:
        self.id = id
        self.idx = idx
        self.entity = entity
    
    def equals(self, string) -> bool:
       return self.value == string

def find_emote_by_idx(idx:int) -> EMOTE:
    return next((emote for emote in list(EMOTE) if emote.idx == idx), None)

def find_emote_by_ide(id:str) -> EMOTE:
    return next((emote for emote in list(EMOTE) if emote.id == id), None)

EMOTES = list(EMOTE)