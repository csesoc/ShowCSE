from Application import db
from flask_login import UserMixin

class Project(db.Document):
    id = db.IntField(required=True)
    name = db.StringField()
    date_uploaded = db.CreatedField()
    primary_image = db.AnythingField(required=False)
    description = db.StringField()
    images = db.ListField(db.AnythingField(required=False))
    # devs = db.SetField(db.DocumentField("User"))
    # stars = db.SetField(db.DocumentField("User"))

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