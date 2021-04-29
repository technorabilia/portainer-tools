from flask import Blueprint, render_template, current_app, send_from_directory

from ..models import AppTemplate

main = Blueprint('main', __name__)


@main.route("/")
def index():
    apptemplates = AppTemplate.query.all()
    return render_template('index.html', apptemplates=apptemplates)


@main.route('/templates/<path:path>')
def host_templates(path):
    return send_from_directory(current_app.config["TEMPLATE_DIR"], path)
