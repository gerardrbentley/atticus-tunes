import json
import datetime
import os
import logging

import click
import psycopg2

from atticus_tunes.app import create_app
from atticus_tunes.db import Database

db = Database(f"{os.getenv('DATABASE_URL')}{os.getenv('DATABASE_NAME')}")

logger = logging.getLogger()


@click.group()
def cli():
    """ Run DB tasks on PostgreSQL using SQLAlchemy. """
    pass


@click.command()
@click.option('--with-test/--no-with-test', default=False, help='Create a test db too?')
def init(with_test):
    """
    Initialize database, optionally with test database as well.
    Does not seed.

    Args:
        with_test (bool): Create a test database
    """
    logger.info('Dropping Tables')
    db.drop_all()
    logger.info('Creating All Tables')
    db.create_all()
    db_uri = f"{os.getenv('DATABASE_URL')}{os.getenv('DATABASE_NAME')}"

    if with_test:
        if not Database.database_exists(db_uri, 'test'):
            logger.info('Creating Test Database')
            Database.create_database(
                db_uri, name='test')
            logger.info('Created Test Database')


@click.command("seed")
def seed():
    logger.info('Seeding Database')


@click.command()
@click.option('--with-test/--no-with-test', default=False, help='Create a test db too?')
@click.pass_context
def reset(ctx, with_test):
    """
    Init and seed in one step. Optionally with test postgres db

    Args:
        ctx ([type]): [description]
        with_test (bool): [Create test database as well]
    """
    logger.info(f'Init and Seed Database, with test? {with_test}')
    ctx.invoke(init, with_test=with_test)
    ctx.invoke(seed)


cli.add_command(init)
cli.add_command(seed)
cli.add_command(reset)
