from flask.ext.classy import FlaskView, route
from flask import render_template, redirect, url_for, flash
from flask_menu.classy import classy_menu_item
from flask_login import current_user, login_required

from Application.models import User
from .forms import UserEditForm

def show_menu():
    return current_user.is_authenticated

class Profile(FlaskView):
    route_base = '/profile'

    @classy_menu_item('frontend-right.account', 'Account', visible_when=show_menu, order=1)
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
        return render_template('.profile/index.html', user=user)

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

            current_user.save()

            flash('Sucessfully updated your details!', 'success')
            return redirect(url_for('.Profile:me'))

        return render_template(".profile/edit_user.html", is_form=True,
            form=form, user=current_user)
