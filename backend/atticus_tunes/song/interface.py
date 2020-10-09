from typing import TypedDict
import uuid
import enum


class Genre(enum.Enum):
    Rock = 1
    Pop = 2
    Rap = 3
    Rb = 4


class SongInterface(TypedDict, total=False):
    """Type Description for Valid Song entries"""

    id: uuid.UUID
    name: str
    genre: Genre
    artist: str
    length: int
    song: str
    ranking: int
