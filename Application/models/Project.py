from Application import db
from User import User

class Project(db.Document):
	name = db.StringField()
	date_uploaded = db.CreatedField()
	primary_image = db.AnythingField(required=False)
	images = db.ListField()
	devs = db.SetField(db.DocumentField(User))