from dataclasses import dataclass
from typing import List


@dataclass
class Artist:
    id: int
    name: str

@dataclass
class ArtistsResponse:
    artists: List[Artist]
