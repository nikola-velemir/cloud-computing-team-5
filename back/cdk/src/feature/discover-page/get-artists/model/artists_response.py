from dataclasses import dataclass
from typing import List


@dataclass
class Artist:
    id: int
    firstName: str
    lastName: str

@dataclass
class ArtistsResponse:
    artists: List[Artist]
