import uuid

import pytest

from .model import Song
from .interface import Genre

from lib.stubs import song_params


class TestSongModel(object):
    @pytest.fixture
    def model(self) -> Song:
        params = song_params()
        return Song(**params)

    def test_Song_create(self, model: Song):
        assert model

    def test_Song_create_with_id(self):
        params = song_params(with_id=True)
        model = Song(**params)
        assert model

    def test_Song_attrs(self, model: Song):
        assert type(model.id) == uuid.UUID
        assert type(model.name) == str
        assert type(model.genre) == Genre
        assert type(model.artist) == str
        assert type(model.length) == int
        assert type(model.song) == str
        assert type(model.ranking) == int
