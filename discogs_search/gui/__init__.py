import os
from flask import Flask
from flask_socketio import SocketIO


socketio = SocketIO()


def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'gjr39dkjn344_!67#')

    from .scanner import main as scanner_blueprint
    app.register_blueprint(scanner_blueprint)

    socketio.init_app(app)
    return app
