from flask.ext.classy import FlaskView, route
from flask import render_template, request
from flask_menu.classy import classy_menu_item
from flask_login import login_required
from .forms import SubmitProjectForm
class Project(FlaskView):
    route_base = '/project'
    
    def index(self):
        return render_template('.project/index.html')

    @classy_menu_item('frontend-right.submit', 'Submit', order=0)
    @login_required
    @route('/submit/', methods=['GET','POST'])
    def submit(self):
        form = SubmitProjectForm()
        print(request.files)
        if form.validate_on_submit():
            print("dksjhfdskjhf")
        return render_template('.project/submit.html', form=form)
