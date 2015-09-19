from flask.ext.classy import FlaskView, route
from flask import render_template

class Profile(FlaskView):
    route_base = '/profile'

    def index(self):
        return render_template('.profile/index.html')
