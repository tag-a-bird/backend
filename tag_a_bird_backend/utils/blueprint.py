from flask import Blueprint

route_blueprint = Blueprint('route_blueprint', __name__,        
    template_folder='templates',
    static_folder='staticbackup')