from flask import Blueprint, render_template

general_bp = Blueprint('general', __name__, template_folder='templates', static_folder='static')

@general_bp.route('/about')
def about():
    return render_template('about.html')