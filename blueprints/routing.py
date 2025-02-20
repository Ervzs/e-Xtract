from flask import Blueprint, render_template

routing_bp = Blueprint('routing', __name__) #initialize blueprint

#02.20.25 Ervzs removed static_folder and template_folder
#create_app() in blueprints/__init__.py already sets static_folder and template_folder for the whole app.
#No need to redefine it for each blueprint.

@routing_bp.route('/disposal-sites') 
def disposal_route():
    return render_template('disposal_sites.html')

