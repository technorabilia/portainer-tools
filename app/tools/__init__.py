import os

from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

socketio = SocketIO()
db = SQLAlchemy()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    socketio.init_app(app)

    from .main.routes import main
    app.register_blueprint(main)
    from .apptemplates.routes import apptemplates
    app.register_blueprint(apptemplates)

    with app.app_context():
        os.makedirs(app.config["TEMPLATE_DIR"], exist_ok=True)
        db.create_all()

    return app
