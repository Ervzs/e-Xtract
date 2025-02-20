from flask import Blueprint, render_template

views_bp = Blueprint('views', __name__) #initialize blueprint

#02.20.25 Ervzs removed static_folder and template_folder
#create_app() in blueprints/__init__.py already sets static_folder and template_folder for the whole app.
#No need to redefine it for each blueprint.

@views_bp.route('/') 
def home():
    return render_template('home.html')

@views_bp.route('/about') 
def about():
    return render_template('about.html')

@views_bp.route('/camera')
def camera():
    return render_template('camera.html')


