import json
import os
import uuid

from flask import url_for

import pytest

from atticus_tunes.app import create_app
from atticus_tunes.db import Database
from atticus_tunes.extensions import db as _db


class ViewTestMixin(object):
    """
    Automatically load in a client, this is common for a lot of
    tests that work with views.
    """
    @pytest.fixture(autouse=True)
    def set_common_fixtures(self, client):
        self.client = client


_db_uri = f"{os.getenv('DATABASE_URL')}test"


@pytest.fixture(scope='session')
def app():
    params = {
        'DEBUG': False,
        'TESTING': True,
        'DATABASE_URI': _db_uri
    }

    _app = create_app(test_config=params)
    _db.init_app(_app)
    _db.drop_all()
    _db.create_all()

    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='function')
def client(app):
    yield app.test_client()
