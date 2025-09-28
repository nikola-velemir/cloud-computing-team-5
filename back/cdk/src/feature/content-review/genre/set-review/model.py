import dataclasses


@dataclasses.dataclass(frozen=True,slots=True)
class SongReviewRecord:
    User:str
    Content:str
    Rating:str
    Timestamp:str
    CoverPath:str
    NameEntity: str

