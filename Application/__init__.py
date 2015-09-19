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

# Setup LDAP Login
from flask.ext.ldap3_login.forms import LDAPLoginForm
from flask_ldap3_login import LDAP3LoginManager
from flask_login import LoginManager, login_user, UserMixin, current_user

# Setup LDAP Configuration Variables. Change these to your own settings.
# All configuration directives can be found in the documentation.
app.config['LDAP_HOST'] = 'ad.unsw.edu.au'             # Hostname of your LDAP Server
app.config['LDAP_BASE_DN'] = 'OU=IDM,DC=ad,DC=unsw,DC=edu,DC=au'       # Base DN of your directory
# app.config['LDAP_USER_DN'] = 'ou=users'                 # Users DN to be prepended to the Base DN
# app.config['LDAP_GROUP_DN'] = 'ou=groups'               # Groups DN to be prepended to the Base DN
app.config['LDAP_BIND_DIRECT_CREDENTIALS'] = True
# app.config['LDAP_USER_RDN_ATTR'] = 'cn'                 # The RDN attribute for your user schema on LDAP
# app.config['LDAP_USER_LOGIN_ATTR'] = 'cn'             # The Attribute you want users to authenticate to LDAP with.
# app.config['LDAP_BIND_USER_DN'] = None                  # The Username to bind to LDAP with
# app.config['LDAP_BIND_USER_PASSWORD'] = None            # The Password to bind to LDAP with

login_manager = LoginManager(app)              # Setup a Flask-Login Manager
ldap_manager = LDAP3LoginManager(app)          # Setup a LDAP3 Login Manager.

from flask import render_template_string, redirect


# Create a dictionary to store the users in when they authenticate
# This example stores users in memory. 
users = {}


# Declare a User Loader for Flask-Login.
# Simply returns the User if it exists in our 'database', otherwise 
# returns None.
@login_manager.user_loader
def load_user(id):
    if id in users:
        return users[id]
    return None


# Declare The User Saver for Flask-Ldap3-Login
# This method is called whenever a LDAPLoginForm() successfully validates.
# Here you have to save the user, and return it so it can be used in the
# login controller.
@ldap_manager.save_user
def save_user(dn, username, data, memberships):
    user = User(dn, username, data)
    users[dn] = user
    return user

# Declare some routes for usage to show the authentication process.

@app.route('/')
def home():
    # Redirect users who are not logged in.
    if not current_user or current_user.is_anonymous():
        return redirect(url_for('login'))

    # User is logged in, so show them a page with their cn and dn.
    template = """
    <h1>Welcome: {{ current_user.data.cn }}</h1>
    <h2>{{ current_user.dn }}</h2>
    """

    return render_template_string(template)

@app.route('/manual_login')
def manual_login():
    # Instead of using the form, you can alternatively authenticate
    # using the authenticate method.
    # This WILL NOT fire the save_user() callback defined above.
    # You are responsible for saving your users.
    app.ldap3_login_manager.authenticate('username','password')

@app.route('/login', methods=['GET','POST'])
def login():
    template = """
    {{ get_flashed_messages() }}
    {{ form.errors }}
    <form method="POST">
        <label>Username{{ form.username() }}</label>
        <label>Password{{ form.password() }}</label>
        {{ form.submit() }}
        {{ form.hidden_tag() }}
    </form>
    """

    # Instantiate a LDAPLoginForm which has a validator to check if the user
    # exists in LDAP. 
    form = LDAPLoginForm()
    if form.validate_on_submit():
        # Successfully logged in, We can now access the saved user object
        # via form.user. 
        login_user(form.user) # Tell flask-login to log them in.
        return redirect('/')  # Send them home

    return render_template_string(template, form=form)

@app.route('/ldap')
def ldap_info():
    pass
