from flask import Flask
from .extract import extract_bp
from .routing import routing_bp
from .views import views_bp
from .detect import detection_bp


def create_app():
    app = Flask(__name__, static_folder='../static', template_folder='../templates')  # Initialize flask app with static and template directories
    
    app.config['SECRET_KEY'] = 'phaethon'

    # Register Blueprints
    app.register_blueprint(extract_bp)
    app.register_blueprint(routing_bp)
    app.register_blueprint(views_bp)
    app.register_blueprint(detection_bp)

    return app
