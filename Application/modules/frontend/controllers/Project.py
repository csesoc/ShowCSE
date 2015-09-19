from flask.ext.classy import FlaskView, route
from flask import render_template

class Project(FlaskView):
    route_base = '/project'
    
    def index(self):
        return render_template('.project/index.html')
