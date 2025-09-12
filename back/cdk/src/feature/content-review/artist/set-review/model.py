import dataclasses


@dataclasses.dataclass(frozen=True,slots=True)
class AlbumReviewRecord:
    User:str
    Content:str
    Rating:str
    Timestamp:str

