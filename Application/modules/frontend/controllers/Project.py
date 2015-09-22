from flask.ext.classy import FlaskView, route
from flask import render_template, request, redirect, url_for, abort, flash, current_app
from flask_menu.classy import classy_menu_item
from flask_login import login_required, current_user
from .forms import SubmitProjectForm, StarForm


from Application.models.Project import Project as DBProject
from Application.models.Project import ProjectImage
from Application import db
from Application.uploads import images
import os

class Project(FlaskView):
    route_base = '/project'
    
    def index(self):
        # return render_template('.project/index.html')
        abort(404)

    @route('/<int:id>/', methods=["GET", "POST"])
    def view_project(self, id):
        project = DBProject.query.get_or_404(id)
        star_form = StarForm()
        if star_form.validate_on_submit():
            if not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()

            if current_user in project.stars.all():
                # remove user from starsa
                project.stars.remove(current_user)
            else:
                # add.
                project.stars.append(current_user)

            db.session.commit()

        
        return render_template('.project/view_project.html', project=project, 
            star_form=star_form)


    @classy_menu_item('frontend-right.submit', 'Submit', order=0)
    @login_required
    @route('/submit/', methods=['GET','POST'], endpoint='Project:submit')
    @route('/<int:id>/edit', methods=['GET','POST'], endpoint='Project:edit')
    def submit(self, id=None):
        project = None
        if id is not None:
            project = DBProject.query.get_or_404(id)

        form = SubmitProjectForm(obj=project)
        if form.validate_on_submit():

            if project is None:
                project = DBProject()

            project.description = form.description.data
            project.download_link = form.download_link.data
            project.website_link = form.website_link.data
            project.demo_link = form.demo_link.data
            project.name = form.name.data

            # Check valid files
            valid_files = True
            for file in request.files.getlist("images"):
                if file.filename:
                    filename, extension = os.path.splitext(file.filename)
                    if not images.extension_allowed(extension[1:].lower()):
                        flash("Image: '{}' is not an allowed file format.".format(file.filename), 'danger')
                        valid_files = False
                        break
                    else:
                        filename = images.save(file)

                        image = ProjectImage(
                            filename=filename,
                            project=project,
                        )
                        db.session.add(image)

            if valid_files:
                if id is None:
                    db.session.add(project)
                    project.devs.append(current_user)
                    flash("Project '{}' created!".format(project.name), 'success')
                else:    
                    flash("Project '{}' updated!".format(project.name), 'success')
                
                db.session.commit()
                return redirect(url_for('.Project:view_project', id=project.id))

        if id is None:
            return render_template('.project/submit.html', form=form, project=project)

        else:
            return render_template('.project/edit/edit.html', form=form, project=project)

    @classy_menu_item('frontend.project.admin.images', 'Images', order=2)
    @route('/<int:id>/edit/images', methods=['GET','POST'])
    def edit_images(self, id):
        return render_template('.project/edit/images.html')

    @classy_menu_item('frontend.project.admin.contributors', 'Contributors', order=3)
    @route('/<int:id>/edit/contributors', methods=['GET','POST'])
    def edit_contributors(self, id):
        return render_template('.project/edit/contributors.html')





