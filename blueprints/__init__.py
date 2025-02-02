from flask import Flask
from .extract import extract_bp
from .routing import routing_bp
from .views import views_bp


__all__ = ["extract_bp", "routing_bp", "views_bp"]

def create_app():
    app = Flask(__name__, static_folder='../static', template_folder='../templates')  # Set template folder explicitly
    
    app.config['SECRET_KEY'] = 'phaethon'

    # Register Blueprints
    app.register_blueprint(extract_bp)
    app.register_blueprint(routing_bp)
    app.register_blueprint(views_bp)

    return app
