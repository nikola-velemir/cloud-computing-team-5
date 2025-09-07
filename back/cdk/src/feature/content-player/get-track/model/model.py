import dataclasses


@dataclasses.dataclass
class TrackResponse:
    id:str
    name:str
    artistNames:list[str]
    audioUrl:str
    duration:int