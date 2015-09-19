from Application import db
from flask_login import UserMixin

class Project(db.Document):
    id = db.IntField(required=True)
    name = db.StringField()
    date_uploaded = db.CreatedField()
    primary_image = db.AnythingField(required=False)
    description = db.StringField()
    images = db.ListField(db.AnythingField(required=False))
    devs = db.SetField(db.DocumentField("User"))
    stars = db.SetField(db.DocumentField("User"))

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

