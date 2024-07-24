from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from functools import wraps
from ...models import Role, QueryConfig
from ...db import db_session
from ...helpers import populate_db_from_coreo
from flask import jsonify

admin_bp = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

def admin_access_required():
    def wrapper(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            if db_session.query(Role).filter(Role.name == 'Admin').first() in current_user.roles:
                print("access: Admin")
            else:
                return jsonify({"msg": "Only the admin can access this page"}), 401
            return fn(*args, **kwargs)
        return decorated_function
    return wrapper

@admin_bp.route('/admin/populate_db', methods=["GET", "POST"])
@login_required
@admin_access_required()
def populate_db():
    if request.method == "GET":
        return render_template('admin/populate_db.html')
    elif request.method == "POST":
        try:
            country = request.form['country']
            populate_db_from_coreo(db_session=db_session, country=country)
            flash("Database populated successfully")
        except Exception as e:
            flash('Error: ' + str(e))
            print(e)
        return render_template('admin/populate_db.html')

@admin_bp.route('/admin', methods=['GET', 'POST'])
@login_required
@admin_access_required()
def set_parameters():
    if request.method == 'GET':
        if db_session.query(QueryConfig).first() is None:
            country = QueryConfig(parameter='country', value='')
            db_session.add(country)
            with_annotation = QueryConfig(parameter='with_annotation', value='False')
            db_session.add(with_annotation)
            in_status = QueryConfig(parameter='in_status', value='')
            db_session.add(in_status)
            not_in_status = QueryConfig(parameter='not_in_status', value='')
            db_session.add(not_in_status)
            db_session.commit()
        return render_template('/admin/admin.html', country=db_session.query(QueryConfig).filter_by(parameter='country').first().value, with_annotation=db_session.query(QueryConfig).filter_by(parameter='with_annotation').first().value, in_status=db_session.query(QueryConfig).filter_by(parameter='in_status').first().value, not_in_status=db_session.query(QueryConfig).filter_by(parameter='not_in_status').first().value)
    elif request.method == 'POST':
        try:
            country = QueryConfig(parameter='country', value=request.form['country'])
            db_session.merge(country)
            with_annotation = QueryConfig(parameter='with_annotation', value=request.form['with_annotation'])
            db_session.merge(with_annotation)
            in_status = QueryConfig(parameter='in_status', value=request.form['in_status'])
            db_session.merge(in_status)
            not_in_status = QueryConfig(parameter='not_in_status', value=request.form['not_in_status'])
            db_session.merge(not_in_status)
            db_session.commit()
            flash("Parameters successfully set.")
            return render_template('/admin/admin.html', country=db_session.query(QueryConfig).filter_by(parameter='country').first().value, with_annotation=db_session.query(QueryConfig).filter_by(parameter='with_annotation').first().value, in_status=db_session.query(QueryConfig).filter_by(parameter='in_status').first().value, not_in_status=db_session.query(QueryConfig).filter_by(parameter='not_in_status').first().value)
        except Exception as e:
            db_session.rollback()
            flash('Error: ' + str(e))
            return render_template('/admin/admin.html', country=db_session.query(QueryConfig).filter_by(parameter='country').first().value, with_annotation=db_session.query(QueryConfig).filter_by(parameter='with_annotation').first().value, in_status=db_session.query(QueryConfig).filter_by(parameter='in_status').first().value, not_in_status=db_session.query(QueryConfig).filter_by(parameter='not_in_status').first().value)