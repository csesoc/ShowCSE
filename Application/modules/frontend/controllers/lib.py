from flask import abort, request, redirect, flash, url_for, render_template
from flask_login import current_user

from Application.models.Project import Project as DBProject
from Application.models.Project import ProjectImage
from Application import db
from Application.uploads import images
import os

from .forms import SubmitProjectForm

def developers_only(project):
	if not project.can_edit_project():
		abort(403)

	return True


def submit_project(id=None):
    project = None
    if id is not None:
        project = DBProject.query.get_or_404(id)

    form = SubmitProjectForm(obj=project)
    if form.validate_on_submit():

        if project is None:
            project = DBProject()
            project.owner = current_user

        project.description = form.description.data
        project.download_link = form.download_link.data
        project.website_link = form.website_link.data
        project.demo_link = form.demo_link.data
        project.name = form.name.data

        # Check valid files
        valid_files = upload_images(project)

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

def upload_images(project):
    """
    Upload Images. Returns False if failed, True if no errors were encountered.
    Will emit flash messages too
    """
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

    return valid_files
