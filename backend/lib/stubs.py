import io
import uuid
from atticus_tunes.song.interface import Genre, SongInterface


def stream_cloud_song(file_path: str) -> io.BytesIO:
    """STUB Given a song path, returns a stream of binary data.
    Stream buffer is discarded when the close() method is called.

    :param file_path: Cloud file path
    :type file_path: str
    :return: Would be song file contents
    :rtype: io.BytesIO
    """
    return io.BytesIO(b"Fake Data Stub")


def song_params(with_id=False, external=False) -> SongInterface:
    """Returns dictionary of suitable test song parameters, optionally with a pre-made uuid

    :return: id, name, genre, artist, length, song, and ranking
    :rtype: SongInterface
    """
    output: SongInterface = {
        'name': 'test song',
        'genre': Genre.Rap,
        'artist': 'test artist name',
        'length': 170,
        'song': '/cloud/file/path.mp3',
        'ranking': 5
    }
    if with_id:
        output['id'] = uuid.uuid4()
    if external:
        output['genre'] = 'Rap'
    return output
