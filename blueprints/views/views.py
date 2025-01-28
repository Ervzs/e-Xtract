from flask import Blueprint, render_template

views = Blueprint('views', __name__, static_folder='static', template_folder='templates')

@views.route('/') 
def home():
    return render_template('home.html')

@views.route('/about') 
def about():
    return render_template('about.html') 

@views.route('/get-started')
def get_started():
    return render_template('get_started.html')
