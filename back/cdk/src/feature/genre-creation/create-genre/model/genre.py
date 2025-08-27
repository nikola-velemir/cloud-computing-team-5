from dataclasses import dataclass

@dataclass
class Genre:
    PK:str
    SK:str
    Name:str
    ImageUrl:str = ''