from flask.ext.classy import FlaskView, route
from flask import render_template, request, redirect, url_for, abort, flash
from flask_menu.classy import classy_menu_item
from flask_login import login_required, current_user
from .forms import SubmitProjectForm


from Application.models.Project import Project as DBProject
from Application import db
from Application.uploads import images
import os

class Project(FlaskView):
    route_base = '/project'
    
    def index(self):
        # return render_template('.project/index.html')
        abort(404)

    @route('/<int:id>/')
    def view_project(self, id):
        project = DBProject.query.get_or_404(id)
        return render_template('.project/view_project.html', project=project)



    @classy_menu_item('frontend-right.submit', 'Submit', order=0)
    @login_required
    @route('/submit/', methods=['GET','POST'])
    def submit(self):
        form = SubmitProjectForm()
        if form.validate_on_submit():
            # Check valid files

            valid_files = True
            for file in request.files.getlist("images"):
                filename, extension = os.path.splitext(file.filename)
                if not images.extension_allowed(extension[1:].lower()):
                    flash("Image: '{}' is not an allowed file format.".format(file.filename), 'danger')
                    valid_files = False

            if valid_files:

                project = DBProject(
                    name=form.name.data,
                    description=form.description.data,
                    download_link=form.download_link.data,
                    website_link=form.website_link.data,
                    demo_link=form.demo_link.data,
                )
                project.devs.append(current_user)
                db.session.add(project)
                db.session.commit()

                return redirect(url_for('.Project:view_project', id=project.id))

        return render_template('.project/submit.html', form=form)
