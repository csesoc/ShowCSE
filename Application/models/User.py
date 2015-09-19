from Application import db
from flask_login import UserMixin

class User(db.Document, UserMixin):
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
	# projects = db.SetField(db.DocumentField())
	# TODO JB: TypeError: __init__() missing 1 required positional argument: 'document_class'