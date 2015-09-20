from Application import db
from .UTCDateTime import UTCDateTime, now


project_users_devs = db.Table('project_users_devs',
    db.Column('project_id', db.Integer, db.ForeignKey('project.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

project_users_stars = db.Table('project_users_stars',
    db.Column('project_id', db.Integer, db.ForeignKey('project.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)


class ProjectImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    project = db.relationship('Project', backref=db.backref('images', lazy='dynamic'))


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), primary_key=True)
    date_uploaded = db.Column(UTCDateTime(), default=now)
    
    description = db.Column(db.Text)

    devs = db.relationship('User', secondary=project_users_devs, 
        backref=db.backref('projects', lazy='dynamic'), lazy='dynamic')
    stars = db.relationship('User', secondary=project_users_stars, 
        backref=db.backref('stars', lazy='dynamic'), lazy='dynamic')


    # Images
    primary_image_id = db.Column(db.Integer, db.ForeignKey('project_image.id'))
    primary_image = db.relationship('ProjectImage')

    # Links
    download_link = db.Column(db.String(255))
    website_link = db.Column(db.String(255))
    demo_link = db.Column(db.String(255))

    #TODO
    tags = db.Column(db.String(255))

