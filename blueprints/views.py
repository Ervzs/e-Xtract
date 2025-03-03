from flask import Blueprint, render_template

views_bp = Blueprint('views', __name__) #initialize blueprint

#02.20.25 Ervzs removed static_folder and template_folder
#create_app() in blueprints/__init__.py already sets static_folder and template_folder for the whole app.
#No need to redefine it for each blueprint.


# Responsible for routing and connecting backend and frontend.
# in home.html line 11, you could see being used 'views.extract'
@views_bp.route('/') 
def home():
    return render_template('home.html')


@views_bp.route("/extract")
def extract():
    return render_template("extract.html")

@views_bp.route("/choose")
def choose_device():
    return render_template("choose_device.html")
