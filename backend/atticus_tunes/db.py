import logging

from flask import current_app, _app_ctx_stack
import psycopg2
from psycopg2.extras import DictCursor, register_uuid

logger = logging.getLogger()

register_uuid()


class Database():
    """Postgresql Database Connection Using Psycopg2"""

    def __init__(self, uri=None, app=None):
        self.database_uri = uri
        self.conn = None
        self.tables = ['client']
        if app is not None:
            self.init_app(app)

    def __repr__(self):
        return f"URI: {self.database_uri} | conn: {self.conn} | app: {current_app} | testing? {current_app.config.get('TESTING')} | app db: {current_app.config.get('DATABASE_URI')}"  # noqa: E501

    def init_app(self, app):
        self.database_uri = app.config.get('DATABASE_URI') or self.database_uri
        app.teardown_appcontext(self.teardown)

    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'postgres_db'):
            ctx.postgres_db.close()

    def connect(self):
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(self.database_uri)
            except psycopg2.DatabaseError as e:
                logger.info(e)
                raise e
            finally:
                logger.info('Connection to Database Opened')

    def drop_all(self):
        self.connect()
        try:
            with self.conn.cursor() as cursor:
                logger.info(f'Drop all: {self.tables}')
                for tablename in self.tables:
                    query = f'DROP TABLE IF EXISTS {tablename} CASCADE;'
                    logger.info(f'doing query: {query}')
                    cursor.execute(query)
                self.conn.commit()
                cursor.close()
        except Exception as e:
            logger.error(e)
            self.conn.rollback()
            raise e

    def create_all(self):
        self.connect()
        queries = [
            "CREATE TABLE client (client_id uuid PRIMARY KEY);"]
        try:
            with self.conn.cursor() as cursor:
                for query in queries:
                    cursor.execute(query)
                    logger.info(f"creating query: {query}")
                self.conn.commit()
                cursor.close()
        except Exception as e:
            logger.error(e)
            self.conn.rollback()
            raise e

    def select_rows(self, query, data=None):
        self.connect()
        try:
            with self.conn.cursor(cursor_factory=DictCursor) as cursor:
                if data:
                    cursor.execute(query, data)
                else:
                    cursor.execute(query)
                records = cursor.fetchall()
                cursor.close()
                return records
        except Exception as e:
            logger.error(e)
            self.conn.rollback()
            raise e

    def insert_rows(self, query, data=None):
        self.connect()
        try:
            with self.conn.cursor(cursor_factory=DictCursor) as cursor:
                if data:
                    cursor.execute(query, data)
                else:
                    cursor.execute(query)
                self.conn.commit()
                cursor.close()
                return cursor.rowcount
        except Exception as e:
            logger.error(e)
            self.conn.rollback()
            raise e

    def update_rows(self, query, data=None):
        self.connect()
        try:
            with self.conn.cursor() as cursor:
                if data:
                    print(query, data)
                    cursor.execute(query, data)
                else:
                    print(query)
                    cursor.execute(query)
                self.conn.commit()
                cursor.close()
                return cursor.rowcount
        except Exception as e:
            logger.error(e)
            self.conn.rollback()
            raise e

    def delete_rows(self, query, data=None):
        self.connect()
        try:
            with self.conn.cursor() as cursor:
                if data:
                    cursor.execute(query, data)
                else:
                    cursor.execute(query)
                self.conn.commit()
                cursor.close()
                return cursor.rowcount
        except Exception as e:
            logger.error(e)
            self.conn.rollback()
            raise e

    @staticmethod
    def database_exists(url, name):
        """Check if postgres database exists using psycopg2 connection

        Args:
            url (str): db connection uri
            name (str): name of database to check

        Returns:
            bool: If database exists in postgres instance
        """
        conn = psycopg2.connect(url)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("SELECT datname FROM pg_database;")
        list_database = cur.fetchall()
        conn.close()
        return (name,) in list_database

    @staticmethod
    def create_database(url, encoding='utf8', name='test'):
        """Creates database in postgres instance using psycopg2 connection url

        Args:
            url (str): db connection uri
            encoding (str, optional): db encoding. Defaults to 'utf8'.
            name (str, optional): Name of database to create. Defaults to 'test'.
        """
        conn = psycopg2.connect(url)
        conn.autocommit = True
        cur = conn.cursor()
        text = f"CREATE DATABASE {name} ENCODING '{encoding}';"
        cur.execute(text)
        conn.close()
