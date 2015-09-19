from flask_wtf import Form
from wtforms import (
    DateField, 
    TextField, 
    SelectField, 
    SubmitField, 
    TextAreaField, 
    StringField, 
    BooleanField,
    IntegerField,
    PasswordField
)
from wtforms import widgets
import wtforms.validators as validators

from flask_ldap3_login.forms import LDAPLoginForm

class LoginForm(LDAPLoginForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.submit.label.text = "Login"
        self.username.label.text = "UNSW zID <small>eg. z1234567</small>"

