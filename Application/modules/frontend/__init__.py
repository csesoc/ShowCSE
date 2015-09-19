from flask_boilerplate_utils.overrides import NestableBlueprint
from flask.ext import menu
from flask_menu.classy import register_flaskview

frontend = NestableBlueprint('frontend', __name__, template_folder="templates", 
    static_folder="static", static_url_path='/resource')

from .controllers.Home import Home
Home.register(frontend)
register_flaskview(frontend, Home)

from .controllers.Profile import Profile
Profile.register(frontend)
register_flaskview(frontend, Profile)

from .controllers.Project import Project
Project.register(frontend)
register_flaskview(frontend, Project)

