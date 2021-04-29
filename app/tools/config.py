import os
from urllib.parse import urljoin


class BaseConfig:
    FLASK_HOST = os.environ.get("FLASK_HOST", "0.0.0.0")
    FLASK_PORT = os.environ.get("FLASK_PORT", "9999")
    SECRET_KEY = os.environ.get("SECRET_KEY", "627eb2cba4110e550aa891285e012b6e")

    CONFIG_DIR = os.environ.get("CONFIG_DIR", "/config")

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{CONFIG_DIR}/tools.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SERVER_URL = os.environ.get("SERVER_URL", "http://localhost")

    PORTAINER_URL = os.environ.get("PORTAINER_URL", SERVER_URL + ":9000")
    PORTAINER_USERNAME = os.environ.get("PORTAINER_USERNAME")
    PORTAINER_PASSWORD = os.environ.get("PORTAINER_PASSWORD")

    SERVER_URL = SERVER_URL + ":" + FLASK_PORT
    TEMPLATE_PATH = "templates"
    TEMPLATE_DIR = os.path.join(CONFIG_DIR, TEMPLATE_PATH)
    TEMPLATE_URL = urljoin(SERVER_URL, TEMPLATE_PATH)

class DevelopmentConfig(BaseConfig):
    pass

class ProductionConfig(BaseConfig):
    pass