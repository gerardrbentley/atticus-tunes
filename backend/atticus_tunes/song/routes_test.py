import uuid

import pytest

from flask import url_for

from atticus_tunes.conftest import ViewTestMixin

from lib.stubs import song_params

from .model import Song
from .service import SongService
from .interface import SongInterface


class TestSongCRUD(ViewTestMixin):
    @pytest.fixture
    def songs(self):
        params = song_params(external=True)
        a = SongService.create(params)
        b = SongService.create(params)
        yield [a, b]

        SongService.delete_by_id(a.id)
        SongService.delete_by_id(b.id)

    def test_Song_get_by_id(self, app, songs):
        response = self.client.get(
            url_for('song.song_api', id=songs[0].id))

        assert response.status_code == 200
        assert response.content_type == 'audio/mpeg'

    def test_Song_get_by_id_fails_bad_id(self, app, songs):
        id = uuid.uuid4()
        response = self.client.get(
            url_for('song.song_api', id=id))
        response_data = response.get_json()

        assert response.status_code == 404
        assert response.content_type == 'application/json'
        assert response_data['message']

    def test_Song_post_works(self, app):
        params = song_params(external=True)
        response = self.client.post(url_for('song.song_api'), json=params)
        response_data = response.get_json()

        SongService.delete_by_id(response_data['id'])
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response_data['name'] == params['name']

    def test_Song_post_fails_bad_input(self, app):
        params: SongInterface = {
            'badId': uuid.uuid4()
        }
        response = self.client.post(url_for('song.song_api'), json=params)
        response_data = response.get_json()

        assert response.status_code == 422
        assert response.content_type == 'application/json'
        assert response_data['message']

    def test_Song_put_works(self, app, songs):
        params = {'name': 'new song', 'length': 700, 'ranking': 2}
        response = self.client.put(
            url_for('song.song_api', id=songs[0].id), json=params)
        response_data = response.get_json()

        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response_data['name'] == 'new song'
        assert response_data['ranking'] == 2

    def test_Song_put_fails_bad_input(self, app, songs):
        params: SongInterface = {
            'badId': uuid.uuid4()
        }
        response = self.client.put(
            url_for('song.song_api', id=songs[0].id), json=params)
        response_data = response.get_json()

        assert response.status_code == 422
        assert response.content_type == 'application/json'
        assert response_data['message']

    def test_Song_delete_works(self, app, songs):
        response = self.client.delete(
            url_for('song.song_api', id=songs[0].id))
        response_data = response.get_json()

        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response_data['message'] == 'Success'

    def test_Song_delete_fails_no_exist(self, app):
        id = uuid.uuid4()
        response = self.client.delete(
            url_for('song.song_api', id=id))
        response_data = response.get_json()

        assert response.status_code == 404
        assert response.content_type == 'application/json'
        assert 'Not Deleted' in response_data['message']
