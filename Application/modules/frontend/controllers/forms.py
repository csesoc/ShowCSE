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
    HiddenField,
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

    download_link = TextField("Download Link", description="(optional)")
    website_link = TextField("Website Link", description="(optional) A link to a website about your project")
    demo_link = TextField("Demo Link", description="(optional) A link to a working demo of your project")

    contributors = TextField("Contributors (zID's)")
    tags = TextField("Tags", description="Space separated")

class UserEditForm(Form):
    website = TextField("Your Website")
    github_username = TextField("Your Github Username")
    email = TextField("Your email", description="Never shown publiclly")
    about = TextAreaField("About you", description="Tell us about yourself!")
    submit = SubmitField("Save changes")
