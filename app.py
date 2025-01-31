from blueprints import create_app
from flask import Flask
from blueprints.extract import extract_bp
from blueprints.routing import routing_bp
from blueprints.views import views_bp

app = create_app()



if __name__ == "__main__":
    app.run(debug=True)  # Debug mode enabled here