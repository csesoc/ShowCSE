from flask.ext.classy import FlaskView, route
from flask import render_template, redirect, url_for, request
from flask_menu.classy import classy_menu_item
from flask_login import current_user, login_required, logout_user, login_user

from .forms import LoginForm

def show_menu():
    return not current_user.is_authenticated

class Security(FlaskView):
    route_base = '/sec'

    @classy_menu_item('frontend-right.account.logout', 'Logout', order=1)
    def logout(self):
        logout_user()
        return redirect(url_for('.Home:index'))

    @classy_menu_item('frontend-right.login', 'Login', order=1, visible_when=show_menu)
    @route('/login', methods=['GET','POST'])
    def login(self):
        form = LoginForm()
        if request.args.get('next'):
            form.next.data = request.args.get('next')

        if form.validate_on_submit():
            login_user(form.user)

        if current_user.is_authenticated:
            if form.next.data:
                return redirect(form.next.data)
            else:
                return redirect(url_for('.Home:index'))

        return render_template('.security/login.html', form=form)

    @login_required
    @route('/me/')
    def me(self):
        return render_template('.profile/index.html', user=current_user)

    @route('/<string:user_id>/')
    def user(self, user_id):
        return render_template('.profile/index.html', user=None)