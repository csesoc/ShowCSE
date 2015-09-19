from Application import db

class Project(db.Document):
    id = db.IntField(required=True)
    name = db.StringField()
    date_uploaded = db.CreatedField()
    primary_image = db.AnythingField(required=False)
    description = db.StringField()
    images = db.ListField(db.AnythingField(required=False))
    devs = db.SetField(db.DocumentField("User"))
    stars = db.SetField(db.DocumentField("User"))

