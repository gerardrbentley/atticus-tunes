import os
import subprocess

import click


@click.command()
@click.argument('path', default=os.path.join('atticus_tunes'))
@click.option('--coverage/--no-coverage', default=True, help='Use Coverage with Pytest?')
def cli(path, coverage):
    """
    Run tests with pytest, optionally with coverage as well

    Args:
        path (str): Path to test directory or file
        coverage (bool): --coverage means run with coverage, --no-coverage means no coverage

    Returns:
        N/A: Subprocess call result
    """
    cmd = f'pytest --cov=/home/app/atticus_tunes {path}' if coverage else f'py.test {path}'
    return subprocess.call(cmd, shell=True)
