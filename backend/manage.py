import os

import click

from atticus_tunes.app import create_app

app = create_app()


cmd_folder = os.path.join(os.path.dirname(__file__), 'cli_commands')
cmd_suffix = '_cmd'


class CLI(click.MultiCommand):
    def list_commands(self, ctx):
        """
        Obtain a list of all available commands.

        :param ctx: Click context
        :return: List of sorted commands
        """
        commands = []

        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py') and filename.endswith(cmd_suffix):
                commands.append(filename[4:-3])

        commands.sort()

        return commands

    def get_command(self, ctx, name):
        """
        Get a specific command by looking up the module.

        :param ctx: Click context
        :param name: Command name
        :return: Module's cli function
        """
        ns = {}

        filename = os.path.join(cmd_folder, f'{name}{cmd_suffix}.py')

        with open(filename) as f:
            code = compile(f.read(), filename, 'exec')
            eval(code, ns, ns)

        return ns['cli']


cli = CLI(help='Commands loaded from cli_commands directory')

if __name__ == "__main__":
    cli()
