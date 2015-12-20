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
    name = TextField("Project Name", [validators.required()])
    description = TextAreaField("Project Description")
    submit = SubmitField("Add Project")
    save = SubmitField("Save Changes")

    download_link = TextField("Download Link", description="(optional) eg. http://mywebsite.com", 
        validators=[
        validators.optional(), 
        validators.Regexp(r'http[s]?://[^\"\']', message="Not a valid URL")])
    website_link = TextField("Website Link", description="(optional) A link to a website about your project. eg. http://mywebsite.com",
        validators=[
            validators.optional(), 
            validators.Regexp(r'http[s]?://[^\"\']', message="Not a valid URL")])
    demo_link = TextField("Demo Link", description="(optional) A link to a working demo of your project. eg. http://mywebsite.com",
        validators=[
            validators.optional(), 
            validators.Regexp(r'http[s]?://[^\"\']', message="Not a valid URL")])

    tags = TextField("Tags", description="Space separated")

class UserEditForm(Form):
    website = TextField("Your Website")
    github_username = TextField("Your Github Username")
    email = TextField("Your email", description="Never shown publiclly")
    about = TextAreaField("About you", description="Tell us about yourself!")
    submit = SubmitField("Save changes")

class StarForm(Form):
    submit = SubmitField("Star")

class EditImages(Form):
    image_id = HiddenField(validators=[validators.required()])
    submit = SubmitField("Delete")

class UploadImages(Form):
    submit = SubmitField("Upload Images")    

class RemoveContributor(Form):
    zid = HiddenField(validators=[validators.required()])
    submit = SubmitField("Remove")

class AddContributor(Form):
    zid = TextField("zID", description="We will attempt to find this user "\
        "on ShowCSE. If they do not have an account, their zID will be replaced "\
        "by their name on their first login.", validators=[validators.required()])
    submit = SubmitField("Add Contributor")    



