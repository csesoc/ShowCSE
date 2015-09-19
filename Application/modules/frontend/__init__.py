from flask_boilerplate_utils.overrides import NestableBlueprint
from flask.ext import menu
from flask_menu.classy import register_flaskview

frontend = NestableBlueprint('frontend', __name__, template_folder="templates", 
    static_folder="static")

# from .controllers.Index import Index
# Index.register(frontend)
# register_flaskview(frontend, Index)

# Pragma - Submodule Registration Start
# Anything after the above line will be removed after cleanup.
# from .modules.learn_flask import learn_flask
# from .modules.examples import examples
# from .modules.cleanup import cleanup
# frontend.register_blueprint(learn_flask, url_prefix='/learn-flask')
# frontend.register_blueprint(examples, url_prefix='/examples')
# frontend.register_blueprint(cleanup, url_prefix='/cleanup')