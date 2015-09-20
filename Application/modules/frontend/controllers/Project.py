from flask.ext.classy import FlaskView, route
from flask import render_template, request, redirect, url_for
from flask_menu.classy import classy_menu_item
from flask_login import login_required
from .forms import SubmitProjectForm

import re
slug_regex_filter = re.compile(r'[^0-9a-z\s\-]')

from Application.models.Project import Project as DBProject

class Project(FlaskView):
    route_base = '/project'
    
    def index(self):
        return render_template('.project/index.html')

    @route('/<string:slug>/')
    def view_project(self, slug):
        return render_template('.project/index.html')



    @classy_menu_item('frontend-right.submit', 'Submit', order=0)
    @login_required
    @route('/submit/', methods=['GET','POST'])
    def submit(self):
        form = SubmitProjectForm()
        if form.validate_on_submit():
            slug = form.name.data.lower()
            slug = slug_regex_filter.sub('', slug).strip()
            slug = slug.replace(' ', '-')

            existing_proj = DBProject.query.filter_by(id=slug).first()
            if existing_proj is not None:
                form.name.errors.append('A project with this name already exists. Please try another')
            else:
                project = DBProject(
                    id=slug,
                    name=form.name.data,
                    description=form.description.data,
                    download_link=form.download_link.data,
                    website_link=form.website_link.data,
                    demo_link=form.demo_link.data,
                )
                project.save()
                return redirect(url_for('.Project:view_project', slug=slug))

        return render_template('.project/submit.html', form=form)
