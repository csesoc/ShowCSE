from flask.ext.classy import FlaskView
from flask import render_template
from flask_menu.classy import classy_menu_item
from Application.models.Project import Project

class Home(FlaskView):
    route_base = '/'

    @classy_menu_item('frontend.home', 'Home', order=0)
    def index(self):
        showcase = Project.query.filter(Project.num_images > 0).order_by(
            Project.id.desc()).limit(3)
        top_projects = Project.query.order_by(Project.num_stars.desc()).limit(10)

        return render_template(
            '.home/index.html', 
            showcase=showcase,
            top_projects=top_projects)

    @classy_menu_item('frontend.directory', 'Directory', order=1)
    def directory(self):
        projects = Project.query.filter(
            Project.name != None # noqa
        ).order_by(Project.name.asc())

        return render_template(
            '.home/directory.html',
            projects=projects)