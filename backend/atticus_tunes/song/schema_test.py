import uuid

import pytest

from .model import Song
from .schema import SongSchema
from .interface import SongInterface, Genre

from lib.stubs import song_params


class TestSongSchema(object):
    def test_SongSchema_exists(self):
        schema = SongSchema(many=False)
        assert schema

    def test_SongSchema_loads_one(self):
        schema = SongSchema(many=False)
        params = song_params(external=True)
        loaded = schema.load(params)

        song = Song(**loaded)

        assert type(song) == Song
        assert type(song.id) == uuid.UUID
        assert song.name == params['name']

    def test_SongSchema_dumps_one(self):
        schema = SongSchema(many=False)
        params = song_params(external=True)
        song_dict = schema.load(params)
        song = Song(**song_dict)
        data = schema.dump(song)

        assert type(data) == dict
        assert data['name'] == params['name']

    def test_SongSchema_loads_many(self,):
        schema = SongSchema(many=True)
        params = song_params(external=True)
        models = schema.load([params, params])
        models = [Song(**param_set) for param_set in models]

        assert isinstance(models, list)
        assert all(isinstance(m, Song) for m in models)
        assert len(models) == 2
        assert models[0].name == params['name']
        assert models[0].name == models[1].name

    def test_SongSchema_dumps_many(self):
        schema = SongSchema(many=True)
        params = song_params(external=True)
        models = schema.load([params, params])
        models = [Song(**param_set) for param_set in models]
        data = schema.dump(models)

        assert isinstance(data, list)
        assert all(isinstance(d, dict) for d in data)
        assert len(data) == 2
        assert data[0]['name'] == params['name']
        assert data[0]['name'] == data[1]['name']
