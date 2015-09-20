from flask.ext.classy import FlaskView, route
from flask import render_template
from flask_menu.classy import classy_menu_item
from Application.models.Project import Project, ProjectImage, project_users_stars
from Application.models.User import User
from Application import db

from sqlalchemy import func

class Home(FlaskView):
    route_base = '/'

    @classy_menu_item('frontend.home', 'Home', order=0)
    def index(self):
        projects = Project.query.order_by(Project.name.asc())
        showcase = Project.query.join(ProjectImage).order_by(Project.id.desc()).limit(3)
        
        # subq = (db.session.query( Project.id.label("project_id"),
        #     func.count(project_users_stars.c.user_id).label("num_stars"))
        #     .outerjoin(project_users_stars).group_by(Project.id)
        # ).subquery("subq")

        # top_projects = (db.session.query(Project, subq.c.num_stars)
        #         .join(subq, Project.id == subq.c.project_id)
        #         .group_by(Project).order_by(subq.c.num_stars.desc())
        #     )
    


        top_projects = Project.query.order_by(Project.num_stars.desc()).limit(10)
        return render_template('.home/index.html', 
            projects=projects,
            showcase=showcase,
            top_projects=top_projects
        )
