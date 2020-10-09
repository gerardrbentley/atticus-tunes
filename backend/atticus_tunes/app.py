import logging
import os

from flask import Flask, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix

from atticus_tunes.song.routes import song
from atticus_tunes.extensions import db


def create_app(test_config=None):
    """Create and return a Flask Application with app factory pattern

    :param test_config: Mapping of override Env Variables, defaults to None
    :type test_config: dict[str, str], optional
    :return: Flask App
    :rtype: Flask
    """
    logging.basicConfig(
        format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s', level=logging.DEBUG)
    app = Flask(__name__)
    app.config.from_object("config.settings")

    if test_config:
        app.config.from_mapping(test_config)

    db.init_app(app)

    app.register_blueprint(song)

    init_middleware(app)

    @app.route("/health")
    def health():
        return jsonify(health="healthy"), 200

    @app.errorhandler(422)
    @app.errorhandler(400)
    def handle_error(err):
        headers = err.data.get('headers', None)
        output = err.data.get('messages', ['Invalid request.'])
        output['message'] = output.pop('json')
        if headers:
            app.logger.info(f"m: {output} head: {headers}")
            return jsonify(output), err.code, headers
        else:
            app.logger.info(f"m: {output}")
            return jsonify(output), err.code

    @app.errorhandler(403)
    @app.errorhandler(404)
    def handle_exception(e):
        return jsonify({'message': str(e), 'code': e.code, 'name': e.name}), e.code

    return app


def init_middleware(app: Flask):
    """Registers Middlewares for requests (mutates the app instance passed in)

    :param app: Flask Application to Modify
    :type app: Flask
    :return: None
    :rtype: None
    """
    app.wsgi_app = ProxyFix(app.wsgi_app)

    return None
