from flask import Flask
from flask_boilerplate_utils import Boilerplate
from flask_menu import Menu
from flask.ext.mongoalchemy import MongoAlchemy

app = Flask(__name__)

from .config import Config
app.config_class = Config
app.config.from_object(app.config_class)


# Use Boilerplate extensions
Boilerplate(app)

# Patch the render_template method too.
# (This gives us relative template rendering for blueprints)
from flask_boilerplate_utils.overrides import monkey_patch_all
monkey_patch_all()

# Setup Flask Menu
Menu(app)

#Setup db
db = MongoAlchemy(app)

# Register blueprints
from Application.modules.frontend import frontend
app.register_blueprint(frontend, url_prefix='')
