from Application import db
from flask_login import UserMixin

from .Project import Project

class User(db.Model, UserMixin):
    dn = db.Column(db.String(255))
    zid = db.Column(db.String(9))
    fullname = db.Column(db.String(50))
    website = db.Column(db.String(255))
    github_username = db.Column(db.String(255))
    email = db.Column(db.String(255))
    program = db.Column(db.String(255))
    admin = db.Column(db.Bool())
    about = db.Column(db.Text())
    
    # projects = db.SetField(db.DocumentField(Project), default=None)
    # stars = db.SetField(db.DocumentField(Project), default=None)
    # followers = db.SetField(db.DocumentField("User"), default=None)
    # following = db.SetField(db.DocumentField("User"), default=None)

    def get_id(self):
        return self.zid
