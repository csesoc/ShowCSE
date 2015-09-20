from flask.ext.classy import FlaskView, route
from flask import render_template, redirect, url_for, flash
from flask_menu.classy import classy_menu_item
from flask_login import current_user, login_required

from Application.models import User
from Application.models import Project
from .forms import UserEditForm

from Application import db
from speaklater import make_lazy_string

@make_lazy_string
def account_text():
    if current_user.is_authenticated:
        return "Account ({})".format(current_user.fullname)
    return "Account"

def show_menu():
    return current_user.is_authenticated

class Profile(FlaskView):
    route_base = '/profile'

    @classy_menu_item('frontend-right.account', account_text, visible_when=show_menu, order=1)
    @classy_menu_item('frontend-right.account.profile', 'My Profile', order=0)
    @login_required
    def index(self):
        return redirect(url_for('.Profile:me'))

    @login_required
    @route('/me/')
    def me(self):
        return render_template('.profile/index.html', user=current_user)

    @route('/<string:user_id>/')
    def user(self, user_id):
        user = User.query.filter(User.zid == user_id).first_or_404()
        projects = None
        if user.projects.count():
            projects = user.projects.order_by(Project.date_uploaded.desc())
        following = False
        if current_user.is_authenticated:
            following = current_user.following.filter_by(zid=user_id).count() != 0
        return render_template('.profile/index.html', user=user, following=following, projects=projects)

    @login_required
    @route('/edit/', methods=['GET', 'POST'])
    def edit(self):
        form = UserEditForm(obj=current_user)

        if form.submit.data and form.validate_on_submit:
            #update the user's details
            current_user.website = form.website.data
            current_user.github_username = form.github_username.data
            current_user.email = form.email.data
            current_user.about = form.about.data

            db.session.add(current_user)
            db.session.commit()

            flash('Sucessfully updated your details!', 'success')
            return redirect(url_for('.Profile:me'))

        return render_template(".profile/edit_user.html", is_form=True,
            form=form, user=current_user)

    @login_required
    @route('/follow/<string:user_id>/')
    def follow(self, user_id):

        following = current_user.following.filter_by(zid=user_id).count()

        if user_id == current_user.zid:
            flash("Error: you cannot follow yourself", 'danger')
            return redirect(url_for('.Profile:user', user_id=user_id))

        if following:
            flash("Error: you already follow this user", 'danger')
            return redirect(url_for('.Profile:user', user_id=user_id))

        #Add follower relationship here
        followee = User.query.get_or_404(user_id)
        current_user.following.append(followee)
        db.session.add(current_user)
        db.session.commit()

        flash("User followed successfully", 'success')
        return redirect(url_for('.Profile:user', user_id=user_id))

    @login_required
    @route('/unfollow/<string:user_id>/')
    def unfollow(self, user_id):

        following = current_user.following.filter_by(zid=user_id).count()

        if user_id == current_user.zid:
            flash("Error: you cannot unfollow yourself", 'danger')
            return redirect(url_for('.Profile:user', user_id=user_id))

        if following:
            #Remove relationship here
            followee = User.query.get_or_404(user_id)
            current_user.following.remove(followee)
            db.session.add(current_user)
            db.session.commit()
            flash("User unfollowed successfully", 'success')
            return redirect(url_for('.Profile:user', user_id=user_id))


        flash("Error: you don't follow this user", 'danger')
        return redirect(url_for('.Profile:user', user_id=user_id))
