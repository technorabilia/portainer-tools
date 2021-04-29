import json
import os

from flask import current_app
from flask_sqlalchemy import event

from .. import db
from . import events
from .forms import AppTemplate


@event.listens_for(AppTemplate.__table__, "after_create")
def create_apptemplates(*args, **kwargs):
    db.session.add(AppTemplate(name="LinuxServer.io",
                   url="https://raw.githubusercontent.com/technorabilia/portainer-templates/main/lsio/templates/templates-2.0.json"))
    db.session.add(AppTemplate(name="Portainer",
                   url="https://raw.githubusercontent.com/portainer/templates/master/templates-2.0.json"))

    template_url = current_app.config["TEMPLATE_URL"]
    filename = "custom.json"
    url = template_url + "/" + filename
    db.session.add(AppTemplate(name="Custom", url=url))

    custom_template = {
        "version": "2",
        "templates": [
            {
                "type": 1,
                "title": "Custom",
                "name": "Custom",
                        "note": "Note",
                        "description": "Description",
                        "platform": "linux",
                        "logo": "",
                        "image": "custom:latest",
                        "env": [
                                {
                                    "name": "Custom",
                                    "label": "Custom",
                                    "default": "Custom",
                                    "description": "Custom"
                                }
                        ],
                "ports": [
                            "9876:9876/tcp"
                        ],
                "volumes": [
                            {
                                "container": "/config",
                                "bind": "/volume1/docker/custom/config"
                            }
                        ],
                "restart_policy": "unless-stopped"
            }
        ]
    }

    template_dir = current_app.config["TEMPLATE_DIR"]
    filepath = os.path.join(template_dir, filename)
    out_templates = json.dumps(custom_template, indent=4)
    with open(filepath, "w") as out_file:
        out_file.write(out_templates)

    db.session.commit()
