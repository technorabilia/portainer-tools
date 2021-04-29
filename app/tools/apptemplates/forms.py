import os

import requests
from flask import current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import HiddenField, StringField, SubmitField, ValidationError
from wtforms.fields.html5 import URLField
from wtforms.validators import URL, DataRequired

from ..models import AppTemplate


class AppTemplateForm(FlaskForm):
    current_name = HiddenField('Current_name')
    name = StringField('Name', validators=[DataRequired()])
    current_url = HiddenField('Current_name')
    url = URLField('URL', validators=[DataRequired(), URL()])
    submit = SubmitField('Submit')

    def validate_name(self, name):
        if name.data != self.current_name.data:
            apptemplate = AppTemplate.query.filter_by(name=name.data).first()
            if apptemplate:
                raise ValidationError(
                    'That name is taken. Please choose a different one.')

    def validate_url(self, url):
        template_dir = current_app.config["TEMPLATE_DIR"]
        template_url = current_app.config["TEMPLATE_URL"]

        base_url, filename = os.path.split(url.data)
        current_base_url, current_filename = os.path.split(
            self.current_url.data)

        if current_base_url.startswith(template_url) and base_url != template_url:
            # url.data = self.current_url.data
            raise ValidationError(
                'You can only change the filename of a self-hosted App Template definition.')

        if url.data != self.current_url.data:
            apptemplate = AppTemplate.query.filter_by(url=url.data).first()
            if apptemplate:
                # url.data = self.current_url.data
                raise ValidationError(
                    'That URL is taken. Please choose a different one.')


class UploadAppTemplateForm(FlaskForm):
    file = FileField('App Template definition file', validators=[FileAllowed(['json'])])
    submit = SubmitField('Submit')
