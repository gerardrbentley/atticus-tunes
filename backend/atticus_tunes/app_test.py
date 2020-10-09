import pytest

from flask import Flask, url_for

from atticus_tunes.conftest import ViewTestMixin


class TestBaseApplication():

    def test_flask_create_app(self, app):
        assert app
        assert type(app) == Flask

    def test_flask_health(self, app, client):
        response = client.get(url_for('health'))
        data = response.get_json()
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert data == {'health': 'healthy'}
