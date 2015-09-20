from Application import db

class Project(db.Document):
    id = db.IntField(required=True)
    name = db.StringField(required=True)
    description = db.StringField(required=True, default=None)

    date_uploaded = db.CreatedField()
    primary_image = db.AnythingField(required=False)
    download_link = db.StringField(required=False, default=None)
    website_link = db.StringField(required=False, default=None)
    demo_link = db.StringField(required=False, default=None)
    tags = db.SetField(db.StringField(), required=False, default=None)
    images = db.ListField(db.AnythingField(required=False), required=False, default=None)
    devs = db.SetField(db.DocumentField("User"), default=None)
    stars = db.SetField(db.DocumentField("User"), default=None)

