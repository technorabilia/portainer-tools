import json

import requests
from flask import current_app


def get_merged_templates(templates):
    if len(templates) < 2:
        message = "Please select two or more App template definitions to merge."
        return [], (True, message)

    message = ""
    template_list = []
    for template in templates:
        template_url = template["url"]

        try:
            response = requests.get(template_url)
            template = json.loads(response.text)
            template_list += template["templates"]
        except Exception as e:
            message = f"Error in {template_url}: {str(e)}"
            return [], (True, message)

    merged_templates = {
        "version": "2",
        "templates": template_list
    }
    return merged_templates, (False, message)


def set_template_url(templates_url):
    base_url = current_app.config["PORTAINER_URL"]
    username = current_app.config["PORTAINER_USERNAME"]
    password = current_app.config["PORTAINER_PASSWORD"]

    try:
        url = base_url + "/api/auth"
        payload = json.dumps({
            "username": username,
            "password": password
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        jwt = json.loads(response.text)["jwt"]

        url = base_url + "/api/settings"
        payload = json.dumps({
            "templatesURL": templates_url
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(jwt)
        }
        response = requests.request("PUT", url, headers=headers, data=payload)
    except Exception as e:
        message = f"{str(e)}"
        return (True, message)

    return (False, "OK")
