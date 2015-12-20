#!./.venv/bin/python3

from Application import app
from ApplicationSampleData import SampleDataCommand
from flask_boilerplate_utils.commands import MainManager


manager = MainManager(app,
    with_default_commands=False)

manager.add_command('data', SampleDataCommand)

from flask.ext.migrate import MigrateCommand
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run(default_command="server")
