import os

from flask_socketio import SocketIO

from tools import create_app, socketio
from tools.config import DevelopmentConfig, ProductionConfig

if os.environ.get('FLASK_ENV') == 'development':
    config = DevelopmentConfig()
else:
    config = ProductionConfig()
app = create_app(config)

if __name__ == '__main__':
    socketio.run(app, port=config.FLASK_PORT, host=config.FLASK_HOST)
