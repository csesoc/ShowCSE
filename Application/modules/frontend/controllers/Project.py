from flask.ext.classy import FlaskView, route
from flask import render_template, request, redirect, abort, flash, current_app
from flask_menu.classy import classy_menu_item
from flask_login import login_required, current_user
from .forms import (
    StarForm, 
    EditImages, 
    UploadImages,
    RemoveContributor,
    AddContributor
)

from .lib import developers_only, submit_project, upload_images

from Application.models.Project import Project as DBProject
from Application.models.User import User
from Application import db


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


    @login_required
    @classy_menu_item('frontend-right.submit', 'Submit', order=0)
    @route('/submit/', methods=['GET','POST'])
    def submit(self):
        return submit_project()

    @login_required
    @classy_menu_item('frontend.project.admin.info', 'Project', order=0)
    @route('/<int:id>/edit/info', methods=['GET','POST'])
    def edit(self, id):
        project = DBProject.query.get_or_404(id)
        developers_only(project)
        return submit_project(id)

    @login_required
    @classy_menu_item('frontend.project.admin.images', 'Images', order=2)
    @route('/<int:id>/edit/images', methods=['GET','POST'])
    def edit_images(self, id):
        project = DBProject.query.get_or_404(id)
        developers_only(project)

        edit_images_form = EditImages(prefix='del_image')
        upload_images_form = UploadImages(prefix='upload_image')

        if edit_images_form.submit.data and edit_images_form.validate_on_submit():
            image = project.images.filter_by(id=edit_images_form.image_id.data).first()
            if image is None:
                abort(400)

            db.session.delete(image)
            db.session.commit()

            flash("Image deleted!", 'success')

        elif upload_images_form.submit.data and upload_images_form.validate_on_submit():
            print("Validation on upload new images")

            valid_files = upload_images(project)
            if valid_files:
                flash("Files uploaded successfully.", 'success')

            db.session.commit()

        return render_template('.project/edit/images.html', project=project, 
            edit_images_form=edit_images_form, upload_images_form=upload_images_form)

    @login_required
    @classy_menu_item('frontend.project.admin.contributors', 'Contributors', order=3)
    @route('/<int:id>/edit/contributors', methods=['GET','POST'])
    def edit_contributors(self, id):
        project = DBProject.query.get_or_404(id)
        developers_only(project)

        add_form = AddContributor(prefix='add')
        remove_form = RemoveContributor(prefix='remove')

        print(request.form)

        if project.can_edit_devs() and add_form.submit.data and add_form.validate_on_submit():
            user = User.query.get(add_form.zid.data)
            if user is None:
                user = User(
                    zid=add_form.zid.data,
                    fullname=add_form.zid.data,
                )
                db.session.add(user)

            if user not in project.devs:
                flash("{} was successfully added as a developer.".format(user.fullname), 'success')
                project.devs.append(user)
            else:
                flash("{} is already a developer".format(user.fullname), "danger")

            db.session.commit()

        elif project.can_edit_devs() and remove_form.submit.data and remove_form.validate_on_submit():
            user = User.query.get(remove_form.zid.data)
            if user is None:
                abort(400)

            print(user in project.devs)

            if user in project.devs and user is not project.owner:
                project.devs.remove(user)
                flash("{} successfully removed.".format(user.fullname), 'success')

            db.session.commit()


        return render_template('.project/edit/contributors.html', project=project,
            add_form=add_form, remove_form=remove_form)





