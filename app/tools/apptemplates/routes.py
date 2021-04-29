import requests
import json
import os

from flask import (Blueprint, current_app, flash, redirect,
                   render_template, request, url_for)
from werkzeug.utils import secure_filename

from .. import db
from ..models import AppTemplate
from .forms import AppTemplateForm, UploadAppTemplateForm
from .utils import set_template_url

apptemplates = Blueprint('apptemplates', __name__)


@apptemplates.route("/apptemplate/create", methods=['GET', 'POST'])
def create_apptemplate():
    form = AppTemplateForm()
    if form.validate_on_submit():
        apptemplate = AppTemplate(name=form.name.data, url=form.url.data)
        db.session.add(apptemplate)
        db.session.commit()

        flash('Your App Template definition has been created.', 'success')
        return redirect(url_for('main.index'))
    return render_template('apptemplate.html', title='Add App Template definition',
                           form=form, legend='Add App Template definition')


@apptemplates.route("/apptemplate/<int:apptemplate_id>/update", methods=['GET', 'POST'])
def update_apptemplate(apptemplate_id):
    apptemplate = AppTemplate.query.get_or_404(apptemplate_id)

    form = AppTemplateForm()
    if form.validate_on_submit():
        apptemplate.name = form.name.data
        apptemplate.url = form.url.data
        db.session.commit()

        template_dir = current_app.config["TEMPLATE_DIR"]
        template_url = current_app.config["TEMPLATE_URL"]
        _, filename = os.path.split(form.url.data)
        current_base_url, current_filename = os.path.split(
            form.current_url.data)

        if current_base_url.startswith(template_url):
            filename = secure_filename(filename)
            if filename != current_filename:
                filepath = os.path.join(template_dir, filename)
                current_filepath = os.path.join(template_dir, current_filename)
                os.rename(current_filepath, filepath)

        flash('Your App Template definition has been updated.', 'success')
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        form.name.data = form.current_name.data = apptemplate.name
        form.url.data = form.current_url.data = apptemplate.url
    return render_template('apptemplate.html', title='Update App Template definition',
                           form=form, legend='Update App Template definition')


@apptemplates.route("/apptemplate/<int:apptemplate_id>/delete", methods=['POST'])
def delete_apptemplate(apptemplate_id):
    apptemplate = AppTemplate.query.get_or_404(apptemplate_id)

    template_dir = current_app.config["TEMPLATE_DIR"]
    template_url = current_app.config["TEMPLATE_URL"]
    base_url, filename = os.path.split(apptemplate.url)

    if base_url.startswith(template_url):
        filepath = os.path.abspath(os.path.join(template_dir, filename))
        if os.path.exists(filepath):
            os.remove(filepath)

    db.session.delete(apptemplate)
    db.session.commit()

    flash('Your App Template definition has been deleted.', 'success')
    return redirect(url_for('main.index'))


@ apptemplates.route("/apptemplate/<int:apptemplate_id>/set", methods=['POST'])
def set_apptemplate(apptemplate_id):
    apptemplate = AppTemplate.query.get_or_404(apptemplate_id)

    (error, message) = set_template_url(apptemplate.url)

    if error:
        flash("Could not set the Portainer App Templates URL. Check your Portainer settings (URL/USERNAME/PASSWORD).", "danger")
    else:
        flash('The App Templates URL has been set in Portainer.', 'success')
    return redirect(url_for('main.index'))


@ apptemplates.route('/apptemplates/upload', methods=['GET', 'POST'])
def upload_apptemplate():
    form = UploadAppTemplateForm()
    if form.validate_on_submit():
        template_dir = current_app.config["TEMPLATE_DIR"]
        template_url = current_app.config["TEMPLATE_URL"]

        filedata = form.file.data
        filename = secure_filename(filedata.filename)
        filedata.save(os.path.join(template_dir, filename))

        url = template_url + "/" + filename
        apptemplate = AppTemplate.query.filter_by(url=url).first()
        if not apptemplate:
            apptemplate = AppTemplate(name=filename, url=url)
            db.session.add(apptemplate)
            db.session.commit()

        flash('Your App Template definition file has been uploaded.', 'success')
        return redirect(url_for('main.index'))

    return render_template('upload.html', title='Upload App Template definition file',
                           form=form, legend='Upload App Template definition file')
