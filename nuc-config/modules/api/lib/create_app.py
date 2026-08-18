from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from lib.api import api
from lib.namespaces.inventory import inventory_ns
from lib.namespaces.players import sessions_ns
from lib.namespaces.status import status_ns
from lib.namespaces.graph import graph_ns
from lib.namespaces.profile import profile_ns

class Config:
    DEBUG = True  # Set to False in production
    RESTX_ERROR_404_HELP = False
    CORS_HEADERS = 'Content-Type'

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    app.testing = True

    # Add namespaces
    api.add_namespace(sessions_ns)
    api.add_namespace(status_ns)
    api.add_namespace(inventory_ns)
    api.add_namespace(graph_ns)
    api.add_namespace(profile_ns)

    # Attach the API to the app
    api.init_app(app)

    socketio = SocketIO(app, cors_allowed_origins='*')

    return app, socketio
