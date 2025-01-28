from flask import Blueprint, render_template

extract = Blueprint('extract', __name__, static_folder='static', template_folder='templates')

@extract.route('/extract')
def upload():
    return render_template('extract.html')

