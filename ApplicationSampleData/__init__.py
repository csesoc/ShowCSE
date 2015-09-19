"""
Provide a command line interface for populating the database
with sample data. 

Accessed via the command line: python run.py data ...
"""

from flask_boilerplate_utils.commands import Command, Manager
SampleDataCommand = Manager(usage="Insert sample data into the database")