from flask.ext.classy import FlaskView, route
from flask import render_template
from flask_menu.classy import classy_menu_item


class Home(FlaskView):
    route_base = '/'

    @classy_menu_item('frontend.home', 'Home', order=0)
    def index(self):
        return render_template('.home/index.html')
