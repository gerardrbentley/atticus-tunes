import uuid

from .interface import Genre


class Song(object):
    """Python Object Representation of a Song"""

    def __init__(self, name: str, genre: Genre, artist: str,
                 length: int, song: str, ranking: int, id: uuid.UUID = None):
        self.id = id or uuid.uuid4()
        self.name = name
        self.genre = genre
        self.artist = artist
        self.length = length
        self.song = song
        self.ranking = ranking
