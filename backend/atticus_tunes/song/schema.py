from marshmallow import fields, Schema, post_load, validate

from .model import Song
from .interface import Genre


class SongSchema(Schema):
    """Represents Marshmallow Schema for Serializing / De-serializing Song Object.
    Assists in validating endpoint inputs
    """

    id = fields.UUID(data_key='id')
    name = fields.String(data_key='name', validate=validate.Length(0, 255))
    genre = fields.String(data_key='genre', validate=validate.OneOf(
        [genre.name for genre in Genre]))
    artist = fields.String(data_key='artist', validate=validate.Length(0, 255))
    length = fields.Int(data_key='length', validate=validate.Range(min=1))
    song = fields.String(data_key='song', validate=validate.Length(1, 2056))
    ranking = fields.Int(data_key='ranking',
                         validate=validate.Range(min=0, max=5))
