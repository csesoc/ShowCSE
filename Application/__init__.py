from flask import Flask
from flask_boilerplate_utils import Boilerplate
from flask_menu import Menu

app = Flask(__name__)

from .config import get_config_class
app.config_class = get_config_class()
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
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)


from flask.ext.migrate import Migrate
migrate = Migrate(app, db)

# Register blueprints
from Application.modules.frontend import frontend
app.register_blueprint(frontend, url_prefix='')

# Setup LDAP Login
from flask.ext.ldap3_login.forms import LDAPLoginForm
from flask_ldap3_login import LDAP3LoginManager
from flask_login import LoginManager, login_user, UserMixin, current_user

login_manager = LoginManager(app)              # Setup a Flask-Login Manager
login_manager.login_view = "frontend.Security:login"
login_manager.login_message = None
ldap_manager = LDAP3LoginManager(app)          # Setup a LDAP3 Login Manager.

from flask import render_template_string, redirect


# Declare a User Loader for Flask-Login.
# Simply returns the User if it exists in our 'database', otherwise 
# returns None.

from .models import User
@login_manager.user_loader
def load_user(username):
    user = User.query.filter(User.zid == username).first()
    return user


# Declare The User Saver for Flask-Ldap3-Login
# This method is called whenever a LDAPLoginForm() successfully validates.
# Here you have to save the user, and return it so it can be used in the
# login controller.
@ldap_manager.save_user
def save_user(dn, username, data, memberships):
    user = load_user(username)
    if user is None:
        user = User(
            zid=username,
        )
        db.session.add(user)

    user.fullname = "{} {}".format(
        data['givenName'][0],
        data['sn'][0],
    )
    user.dn = dn
    user.program = "??"
    user.has_logged_in = True
    db.session.commit()
    return user

# Uploads
from .uploads import images
from flask.ext.uploads import configure_uploads, patch_request_class
patch_request_class(app)

#Markdown
from flask.ext.misaka import Misaka
Misaka(app, escape=True, autolink=True)


if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    mail_handler = SMTPHandler('127.0.0.1',
                               'admin@showc.se',
                               app.config.get('DEBUG_EMAILS'), 
                               '{} Failed'.format(app.config.get('APP_NAME')))
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)
