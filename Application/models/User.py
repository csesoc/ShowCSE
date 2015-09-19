from Application import db
from flask_login import UserMixin

from .Project import Project

class User(db.Document, UserMixin):
    dn = db.StringField()
    zid = db.StringField(required=True)
    fullname = db.StringField(required=True)
    website = db.StringField(required=False, default=None)
    github_username = db.StringField(required=False, default=None)
    email = db.StringField(required=False, default=None)
    
    program = db.StringField(required=False, default=None)
    admin = db.BoolField(default=False)
    # projects = db.SetField(db.DocumentField(Project))
    about = db.StringField(required=False, default=None)
    # stars = db.SetField(db.DocumentField(Project))
    # followers = db.SetField(db.DocumentField("User"))
    # following = db.SetField(db.DocumentField("User"))

    def get_id(self):
        return self.zid
