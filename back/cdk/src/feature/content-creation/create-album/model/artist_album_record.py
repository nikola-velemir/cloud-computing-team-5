import dataclasses


@dataclasses.dataclass
class ArtistAlbumRecord:
    PK:str
    SK:str
    GenreIds:list[str]
    Title:str
    ReleaseDate:str
    ImageType:str