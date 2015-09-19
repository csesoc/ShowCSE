from Application import db
from flask_login import UserMixin

from .Project import Project

class User(db.Document, UserMixin):
    dn = db.StringField()
    zid = db.StringField()
    firstname = db.StringField()
    surname = db.StringField()
    website = db.StringField()
    github = db.StringField()
    email = db.StringField()
    program = db.StringField()
    admin = db.BoolField()
    projects = db.SetField(db.DocumentField(Project))
    about = db.StringField()
    stars = db.SetField(db.DocumentField(Project))
    followers = db.SetField(db.DocumentField("User"))
    following = db.SetField(db.DocumentField("User"))