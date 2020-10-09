from flask import Blueprint, jsonify, request, current_app, abort, Response
from flask.views import MethodView

from webargs import fields, validate
from webargs.flaskparser import use_kwargs

from lib.utils_views import use_args_json, register_api
from lib.stubs import stream_cloud_song

from .schema import SongSchema
from .service import SongService
from .model import Song
from .interface import SongInterface

song = Blueprint('song', __name__, url_prefix='')


class SongAPI(MethodView):
    @use_kwargs({'id': fields.UUID(required=True)}, location='view_args')
    def get(self, id):
        """Responds to HTTP GET request at /songs/{id}, where {id} is a placeholder for a valid song ID.
        Returns Binary Stream response if successful, else json with error message and error status
        """
        song: Song = SongService.get_by_id(id)

        if song:
            try:
                return Response(stream_cloud_song(song.song), mimetype='audio/mpeg')
            except Exception as e:
                current_app.logger.error(e)
                abort(
                    404, description=f"Cloud Service Could Not Find Song File: {song.song}")
        else:
            abort(404, description="Song Not Found")

    @use_args_json(SongSchema)
    def post(self, args: SongInterface):
        """Responds to HTTP POST request at /songs/ with valid JSON data to create a Song.
        Attempts to Create a database entry for the input data and returns it if successful.
        """
        created: Song = SongService.create(args)
        if created:
            schema = SongSchema(many=False)
            output = schema.dump(created)
            return jsonify(output), 200
        else:
            abort(500, description="Could Not Create Resource")

    @use_kwargs({'id': fields.UUID(required=True)}, location='view_args')
    @use_args_json(SongSchema)
    def put(self, args: SongInterface, id):
        """Responds to HTTP PUT request at /songs/{id} where {id} is a valid Song ID,
        with valid JSON data to update the given Song's properties.
        Attempts to update the Database record for the given ID
        using the new attributes, returning the full updated Song if successful.
        """
        to_update = SongService.get_by_id(id)

        updated: Song = SongService.update(to_update, args)
        if updated:
            schema = SongSchema(many=False)
            output = schema.dump(updated)
            return jsonify(output), 200
        else:
            abort(404, description="Could Not Update Resource")

    @use_kwargs({'id': fields.UUID(required=True)}, location='view_args')
    def delete(self, id):
        """Responds to HTTP DELETE request at /songs/{id} where {id} is a valid Song ID.
        Attempts to Delete the Database record for the given ID,
        and returns 200 with success message if so.
        """
        deleted = SongService.delete_by_id(id)
        if deleted:
            return jsonify(message='Success'), 200
        else:
            return abort(404, description='The Resource Was Not Deleted')


view_func = SongAPI.as_view('song_api')
song.add_url_rule('/songs/', view_func=view_func, methods=['POST'])
song.add_url_rule('/songs/<uuid:id>', view_func=view_func,
                  methods=['GET', 'PUT', 'DELETE'])
