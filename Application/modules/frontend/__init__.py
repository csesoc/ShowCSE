from flask_boilerplate_utils.overrides import NestableBlueprint
from flask_menu.classy import register_flaskview

from .controllers.Home import Home
from .controllers.Profile import Profile
from .controllers.Project import Project
from .controllers.Security import Security

frontend = NestableBlueprint(
    'frontend', __name__, template_folder="templates", 
    static_folder="static", static_url_path='/resource')


Home.register(frontend)
register_flaskview(frontend, Home)

Profile.register(frontend)
register_flaskview(frontend, Profile)

Project.register(frontend)
register_flaskview(frontend, Project)

Security.register(frontend)
register_flaskview(frontend, Security)

