from Application import db

class User(db.Document):
	dn = db.StringField()
	zid = db.StringField()
	firstname = db.StringField()
	surname = db.StringField()
	degree = db.StringField()
	website = db.StringField()
	github = db.StringField()
	email = db.StringField()
	program = db.StringField()
	admin = db.BoolField()
	projects = db.SetField(db.DocumentField())