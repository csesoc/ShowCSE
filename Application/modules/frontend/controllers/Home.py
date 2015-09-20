from flask.ext.classy import FlaskView, route
from flask import render_template
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
        projects = Project.query.order_by(Project.name.asc())
        showcase = Project.query.join(ProjectImage).order_by(Project.id.desc()).limit(3)
        top_projects = Project.query.order_by(Project.num_stars.desc()).limit(10)

        # following_subquery = db.session.query(users_followers).filter_by(
            # follower_id=current_user.zid
        # ).all()

        # print(following_subquery)


        # following_projects = Project.query.filter(
        #     Project.
        # ).order_by(Project.id.desc()).limit(10)

        return render_template('.home/index.html', 
            projects=projects,
            showcase=showcase,
            top_projects=top_projects
        )
