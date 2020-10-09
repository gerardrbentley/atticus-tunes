from typing import List
import uuid

from psycopg2.sql import SQL, Identifier

from atticus_tunes.extensions import db
from .model import Song
from .interface import SongInterface


class SongService():
    @staticmethod
    def get_all() -> List[Song]:
        """Returns List of Song python object Models

        :return: All Songs in Database
        :rtype: List[Song]
        """
        query = "SELECT * FROM songs;"
        try:
            out = [Song(**params) for params in db.select_rows(query)]
            return out
        except Exception:
            return []

    @staticmethod
    def get_by_id(id: uuid.UUID) -> Song:
        """Returns a single Song with matching id if it exists, else None

        :param id: id to match in database
        :type id: uuid.UUID
        :return: Song that has id equal to input id
        :rtype: Song
        """
        query = "SELECT * FROM songs WHERE id = (%s);"
        data = (id,)
        try:
            out = db.select_rows(query, data)
            out = out[0]
            out = Song(**out)
            return out
        except IndexError:
            return None

    @staticmethod
    def update(song: Song, update_dict: SongInterface) -> Song:
        """Updates a single Song database entry with new columns.
        Returns updated python object Song model

        :param song: Model of Song to update
        :type song: Song
        :param update_dict: Attributes / columns to update with new values
        :type update_dict: SongInterface
        :return: The Model with updated attributes
        :rtype: Song
        """
        try:
            set_format = ",".join(
                [f"{key}=(%s)" for key in update_dict.keys()])
            data_list = []
            old_id = song.id
            for key, value in update_dict.items():
                # set_format += f"{key}=(%s) "
                setattr(song, key, value)
                data_list.append(value)

            data_list.append(old_id)
            query = "UPDATE songs SET " + \
                set_format + " WHERE id=(%s);"
            data = tuple(data_list)
            num_updated = db.update_rows(query, data)
            print(song.name)
            if num_updated == 1:
                return song
            else:
                return None
        except Exception:
            return None

    @ staticmethod
    def delete_by_id(id: uuid.UUID) -> uuid.UUID:
        """Deletes a single Song database entry with matching id.
        Returns the id that was deleted if successful, else None

        :param id: id of the Song to delete
        :type id: uuid.UUID
        :return: the input id if successful, else None
        :rtype: uuid.UUID
        """
        try:
            query = "DELETE FROM songs WHERE id = (%s);"
            data = (id,)
            num_deleted = db.delete_rows(query, data)
            if num_deleted == 1:
                return id
            else:
                return None
        except Exception:
            return None

    @ staticmethod
    def create(params: SongInterface) -> Song:
        """Creates a single Song in the database and returns python object model.

        :param params: Dict of values pertaining to creating a Song
        :type params: SongInterface
        :return: Python object Model of Song if successful, else None
        :rtype: Song
        """
        print('create', params)
        try:
            model = Song(**params)
            columns = list(map(Identifier, params.keys()))
            columns = [Identifier('id'), *columns]
            values = tuple([model.id, *params.values()])
            query = SQL("INSERT INTO songs({cols}) VALUES (%s,%s,%s,%s,%s,%s,%s)").format(
                cols=SQL(',').join(columns)
            )
            num_created = db.insert_rows(query, values)
            if num_created == 1:
                return model
            else:
                return None
        except Exception:
            return None
