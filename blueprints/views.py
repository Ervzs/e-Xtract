from flask import Blueprint, render_template

views_bp = Blueprint('views', __name__, static_folder='static', template_folder='templates')

@views_bp.route('/') 
def home():
    return render_template('home.html')

@views_bp.route('/about') 
def about():
    return render_template('about.html') 

