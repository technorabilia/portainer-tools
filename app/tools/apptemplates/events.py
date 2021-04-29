import json
import os

import requests
from flask import current_app, flash

from .. import db, socketio
from ..models import AppTemplate
from .utils import get_merged_templates


@socketio.on("merge templates")
def merge_templates(templates):
    merged_templates, (error, message) = get_merged_templates(templates)
    if error:
        socketio.emit('merge response', {"error": error, "message": message})
        return

    template_dir = current_app.config["TEMPLATE_DIR"]
    template_url = current_app.config["TEMPLATE_URL"]

    apptemplate = AppTemplate.query.filter_by(name="Merged").first()
    if apptemplate:
        _, filename = os.path.split(apptemplate.url)
        filepath = os.path.join(template_dir, filename)

    else:
        filename = "merged.json"
        filepath = os.path.join(template_dir, filename)

        url = template_url + "/" + filename
        apptemplate = AppTemplate.query.filter_by(url=url).first()
        if not apptemplate:
            apptemplate = AppTemplate(name="Merged", url=url)
            db.session.add(apptemplate)
            db.session.commit()

    out_templates = json.dumps(merged_templates, indent=4)
    with open(filepath, "w") as out_file:
        out_file.write(out_templates)

    socketio.emit('merge response', {
                  "error": error, "message": f'Your App Template definitions have been merged in {filename}.'})
