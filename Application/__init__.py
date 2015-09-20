from flask import Flask
from flask_boilerplate_utils import Boilerplate
from flask_menu import Menu

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
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

# Register blueprints
from Application.modules.frontend import frontend
app.register_blueprint(frontend, url_prefix='')

# Setup LDAP Login
from flask.ext.ldap3_login.forms import LDAPLoginForm
from flask_ldap3_login import LDAP3LoginManager
from flask_login import LoginManager, login_user, UserMixin, current_user

# Setup LDAP Configuration Variables. Change these to your own settings.
# All configuration directives can be found in the documentation.
app.config['LDAP_HOST'] = 'ad.unsw.edu.au'             # Hostname of your LDAP Server
app.config['LDAP_BASE_DN'] = 'OU=IDM,DC=ad,DC=unsw,DC=edu,DC=au'       # Base DN of your directory
app.config['LDAP_USER_DN'] = 'OU=IDM_People'                 # Users DN to be prepended to the Base DN
# app.config['LDAP_GROUP_DN'] = 'ou=groups'               # Groups DN to be prepended to the Base DN
app.config['LDAP_BIND_DIRECT_CREDENTIALS'] = True
app.config['LDAP_BIND_DIRECT_SUFFIX'] = "@ad.unsw.edu.au"
app.config['LDAP_BIND_DIRECT_GET_USER_INFO'] = True
app.config['LDAP_USER_SEARCH_SCOPE'] = "SEARCH_SCOPE_WHOLE_SUBTREE"
app.config['LDAP_USER_LOGIN_ATTR'] = 'cn'
app.config['LDAP_GET_USER_ATTRIBUTES'] = ['dn', 'cn', 'memberOf', 'givenName', 'sn']


login_manager = LoginManager(app)              # Setup a Flask-Login Manager
login_manager.login_view = "frontend.Security:login"
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
            dn=dn,
            zid=username,
        )
        db.session.add(user)

    user.fullname = "{} {}".format(
        data['givenName'][0],
        data['sn'][0],
    )
    user.program = "??"
    db.session.commit()
    return user

db.create_all()

# Uploads
from .uploads import images
from flask.ext.uploads import configure_uploads, patch_request_class
patch_request_class(app)

#Markdown
from flask.ext.misaka import Misaka
Misaka(app)
