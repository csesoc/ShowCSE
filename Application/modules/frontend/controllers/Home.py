from flask.ext.classy import FlaskView, route
from flask import render_template

class Home(FlaskView):
    route_base = '/'

    def index(self):
        return render_template('.home/index.html')
