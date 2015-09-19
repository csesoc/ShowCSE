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
    PasswordField,
    HiddenField
)
from wtforms import widgets
import wtforms.validators as validators

from flask_ldap3_login.forms import LDAPLoginForm

class LoginForm(LDAPLoginForm):

    next = HiddenField()

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.submit.label.text = "Login"
        self.username.label.text = "UNSW zID <small>eg. z1234567</small>"


class SubmitProjectForm(Form):
    name = TextField("Project Name")
    description = TextAreaField("Project Description")
    submit = SubmitField("Add Project")

    download_link = TextField("Download Link")
    website_link = TextField("Website Link")
    demo_link = TextField("Demo Link")

    contributors = TextField("Contributors (zID's)")
    tags = TextField("Tags", description="Space separated")