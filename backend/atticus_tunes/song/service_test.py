from typing import List
import uuid

import pytest

from .model import Song
from .service import SongService
from .interface import SongInterface

from lib.stubs import song_params


class TestSongService(object):

    def test_Song_create_works(self, app):
        params = song_params(external=True)
        song = SongService.create(params)
        results: List[Song] = SongService.get_all()

        SongService.delete_by_id(song.id)
        assert len(results) == 1
        assert song.name == params['name']

    def test_Song_create_fails_bad_input(self, app):
        params = dict(ranking=6)
        song = SongService.create(params)
        results: List[Song] = SongService.get_all()

        assert len(results) == 0
        assert song is None

    def test_Song_get_all(self, app):
        params = song_params(external=True)
        song_1 = SongService.create(params)
        song_2 = SongService.create(params)
        results: List[Song] = SongService.get_all()

        SongService.delete_by_id(song_1.id)
        SongService.delete_by_id(song_2.id)
        assert len(results) == 2
        assert all(lambda x: x['name'] == params['name'] for x in results)

    def test_Song_get_all_no_results(self, app):
        results: List[Song] = SongService.get_all()

        assert len(results) == 0

    def test_Song_update_works(self, app):
        params = song_params(external=True)
        old_song = SongService.create(params)

        params_2 = {'name': 'other test name'}
        song = SongService.update(old_song, params_2)

        SongService.delete_by_id(old_song.id)
        assert song.name == 'other test name'
        assert old_song.name == 'other test name'

    def test_Song_update_fails(self, app):
        params = song_params(external=True)
        model = SongService.create(params)

        params_2 = dict(ranking=6)
        song = SongService.update(model, params_2)

        SongService.delete_by_id(model.id)
        assert song is None
        assert model.name == params['name']

    def test_Song_delete_by_id_works(self, app):
        params = song_params(external=True)
        song_1 = SongService.create(params)
        song_2 = SongService.create(params)

        SongService.delete_by_id(song_1.id)
        results: List[Song] = SongService.get_all()

        id_2 = SongService.delete_by_id(song_2.id)

        assert len(results) == 1
        assert results[0].id == id_2

    def test_Song_delete_by_id_fails(self, app):
        params = song_params(external=True)
        model = SongService.create(params)

        id_2 = uuid.uuid4()
        id = SongService.delete_by_id(id_2)
        results: List[Song] = SongService.get_all()

        SongService.delete_by_id(model.id)

        assert len(results) == 1
        assert results[0].id == model.id
        assert id is None
