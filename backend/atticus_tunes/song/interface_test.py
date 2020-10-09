import uuid

import pytest

from .model import Song
from .interface import SongInterface

from lib.stubs import song_params


class TestSongInterface(object):
    @pytest.fixture
    def interface(self) -> SongInterface:
        params = song_params(with_id=True)
        return SongInterface(**params)

    def test_SongInterface_create(self, interface: SongInterface):
        assert interface

    def test_SongInterface_to_model(self, interface: SongInterface):
        model = Song(**interface)
        assert model

    def test_SongInterface_to_model_no_id(self):
        params = song_params()
        interface = SongInterface(**params)
        model = Song(**interface)
        assert model
