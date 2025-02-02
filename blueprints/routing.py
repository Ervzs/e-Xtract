from flask import Blueprint, render_template

routing_bp = Blueprint('routing', __name__, static_folder='static', template_folder='templates') #initialize blueprint

@routing_bp.route('/disposal-sites') 
def disposal_route():
    return render_template('disposal_sites.html')

