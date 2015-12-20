from flask.ext.classy import FlaskView, route
from flask import render_template, request
from flask_menu.classy import classy_menu_item
from Application.models.Project import Project, ProjectImage, project_users_stars
from Application.models.User import User, users_followers
from Application import db
from flask_login import current_user
from sqlalchemy import func

class Home(FlaskView):
    route_base = '/'

    @classy_menu_item('frontend.home', 'Home', order=0)
    def index(self):
        showcase = Project.query.filter(Project.num_images > 0).order_by(
            Project.id.desc()).limit(3)
        top_projects = Project.query.order_by(Project.num_stars.desc()).limit(10)

        return render_template('.home/index.html', 
            showcase=showcase,
            top_projects=top_projects
        )

    @classy_menu_item('frontend.directory', 'Directory', order=0)
    def directory(self):
        projects = Project.query.filter(Project.name != None).order_by(
            Project.name.asc())

        return render_template('.home/directory.html',
            projects=projects)