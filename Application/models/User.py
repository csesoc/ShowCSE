from Application import db
from flask_login import UserMixin

from .Project import Project

users_followers = db.Table('users_followers',
    db.Column('follower_id', db.String(20), db.ForeignKey('user.zid')),
    db.Column('followee_id', db.String(20), db.ForeignKey('user.zid'))
)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    dn = db.Column(db.String(255))
    zid = db.Column(db.String(20), primary_key=True)
    fullname = db.Column(db.String(50))
    website = db.Column(db.String(255))
    github_username = db.Column(db.String(255))
    email = db.Column(db.String(255))
    program = db.Column(db.String(255))
    admin = db.Column(db.Boolean())
    about = db.Column(db.Text())
    following = db.relationship('User', secondary=users_followers,
        primaryjoin=zid==users_followers.c.follower_id,
        secondaryjoin=zid==users_followers.c.followee_id,
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    stars = db.relationship('Project', secondary='project_users_stars', 
        lazy='dynamic')
    projects = db.relationship('Project', secondary='project_users_devs', lazy='dynamic')

    def get_id(self):
        return self.zid

    def __hash__(self):
        return hash(self.zid)
