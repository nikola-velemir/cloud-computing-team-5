import dataclasses


@dataclasses.dataclass
class TrackResponse:
    id:str
    name:str
    artistNames:list[str]
    url:str
    duration:int