from flask import Blueprint, render_template

dispose = Blueprint('dispose', __name__, static_folder='static', template_folder='templates')

@dispose.route('/disposal-sites') 
def disposal_route():
    return render_template('disposal_sites.html')

