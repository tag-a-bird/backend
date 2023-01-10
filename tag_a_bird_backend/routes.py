from os import getenv
from flask import request, jsonify, render_template, flash, url_for, redirect, Blueprint, session
from flask_login import login_user, login_required, logout_user, current_user
from utils.validate_email import check_email
from utils.helpers import populate_db_from_coreo
import datetime
import uuid
from utils.blueprint import route_blueprint
from utils.models import Role, User, QueryConfig, Record, Annotation
from main import login_manager, limiter
from utils.db import db_session, func
from utils.species import most_possible_birds, other_possible_birds
from utils.flags import flags_list
from functools import wraps

def admin_access_required():
    def wrapper(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            if session.get("role") == 'Admin':
                print("access: Admin")
            else:
                return jsonify({"msg": "Only the admin can access this page"}), 401
            return fn(*args, **kwargs)
        return decorated_function
    return wrapper

@login_manager.user_loader
def load_user(user_id):
    return db_session.query(User).get(user_id)

route_blueprint = Blueprint('route_blueprint', __name__,        
    template_folder='templates',
    static_folder='staticbackup')

@route_blueprint.route('/about')
def about():
    return render_template('about.html')

@route_blueprint.route('/api/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and len(request.form['password']) > 7:
        if check_email(request.form['email']):
            db_session.rollback()
            try:
                user = User(
                        id  = uuid.uuid4(),
                        username = request.form['username'],
                        email = request.form['email'],
                        created_on = datetime.datetime.now()
                        )
                user.set_password(request.form['password'])
                db_session.add(user)
                db_session.commit()
                login_user(user)
                return redirect(url_for('route_blueprint.about'))
            except Exception as e:
                db_session.rollback()
                flash('Error: ' + str(e))
                return render_template('auth/register.html')
        else:
            flash("The email seems to be incorrect!")
            return render_template('auth/register.html') # this clears the entire form, fix later!
    elif request.method == 'POST' and len(request.form['password']) < 8:
        flash("The password must be at least 8 characters long!")
        return render_template('auth/register.html') # this clears the entire form, fix later!
    elif request.method == 'GET':
        if current_user.is_authenticated:
            return render_template('about.html') 
        return render_template('auth/register.html')

@route_blueprint.route('/api/login', methods = ["POST", "GET"])
@limiter.limit("5 per hour", deduct_when=lambda response: response.status_code != 200)
def login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            user = db_session.query(User).filter_by(email=email).first()
            if user.email == getenv("ADMIN_CREDENTIALS_EMAIL"):
                r = db_session.query(Role).get(1)
                session['role'] = r.name
            if not user or not user.verify_password(password):
                return jsonify({"msg": "Bad email or password"}), 401
            login_user(user)
            return redirect(url_for('route_blueprint.about'))
        except Exception as e:
            print(e)
            return jsonify({"msg": "Bad email or password"}), 401
    elif request.method == 'GET':
        if current_user.is_authenticated:
            return render_template('about.html')  
        # for debugging, to check x-ratelimit-remainin header
        # resp = requests.request('GET', 'http://localhost:5000/api/login')
        # pprint.pprint(resp.headers)
        return render_template('auth/login.html')

@route_blueprint.route('/api/logout')
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('route_blueprint.login'))

@route_blueprint.route('/admin/populate_db', methods = ["GET", "POST"])
@login_required
@admin_access_required()
def populate_db():
    if request.method == "GET":
        return render_template('admin/populate_db.html')
    elif request.method == "POST":
        try:
            country = request.form['country']
            populate_db_from_coreo(db_session=db_session, country=country)
        except Exception as e:
            flash('Error: ' + str(e))
            print(e)
        return render_template('admin/populate_db.html')

@route_blueprint.route('/admin', methods=['GET', 'POST'])
@login_required
@admin_access_required()
def set_parameters():
    if request.method == 'GET':
        if db_session.query(QueryConfig).first() is None:
            db_session.add_all([
                QueryConfig(parameter='country', value=''),
                QueryConfig(parameter='with_annotation', value='False'),
                QueryConfig(parameter='in_status', value=''),
                QueryConfig(parameter='not_in_status', value='')
            ])
            db_session.commit()
        return render_template('/admin/admin.html' , country = db_session.query(QueryConfig).filter_by(parameter='country').first().value, with_annotation = db_session.query(QueryConfig).filter_by(parameter='with_annotation').first().value, in_status = db_session.query(QueryConfig).filter_by(parameter='in_status').first().value, not_in_status = db_session.query(QueryConfig).filter_by(parameter='not_in_status').first().value)
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
            return render_template('/admin/admin.html' , country = db_session.query(QueryConfig).filter_by(parameter='country').first().value, with_annotation = db_session.query(QueryConfig).filter_by(parameter='with_annotation').first().value, in_status = db_session.query(QueryConfig).filter_by(parameter='in_status').first().value, not_in_status = db_session.query(QueryConfig).filter_by(parameter='not_in_status').first().value)
        except Exception as e:
            db_session.rollback()
            flash('Error: ' + str(e))
            return render_template('/admin/admin.html' , country = db_session.query(QueryConfig).filter_by(parameter='country').first().value, with_annotation = db_session.query(QueryConfig).filter_by(parameter='with_annotation').first().value, in_status = db_session.query(QueryConfig).filter_by(parameter='in_status').first().value, not_in_status = db_session.query(QueryConfig).filter_by(parameter='not_in_status').first().value)
    
@route_blueprint.route('/annotate', methods = ["GET", "POST"])
@login_required
def annotate():
    def get_record(countries, with_annotation: bool=True, not_in_status: list = ['draft', 'reported'], in_status: list = ['questioned']):
        try:
            record = db_session.query(Record).filter(Record.country == func.any(countries)).filter(Record.species != None).order_by(func.random()).first()
            users_annotations = db_session.query(User).filter(current_user.id == User.id).first().annotations
            if users_annotations:
                related_records = [db_session.query(Record).filter(Record.id == annotation.recording_id).first() for annotation in users_annotations]
                while record in related_records:
                    record = db_session.query(Record).filter(Record.country == func.any(countries)).filter(Record.species != None).order_by(func.random()).first()
            return record
        except AttributeError:
            flash("No records found")
            return None
    if request.method == "GET":
        countries = db_session.query(QueryConfig).filter_by(parameter='country').first().value.split(',')
        with_annotation = db_session.query(QueryConfig).filter_by(parameter='with_annotation').first().value
        not_in_status = db_session.query(QueryConfig).filter_by(parameter='not_in_status').first().value.split(',')
        in_status = db_session.query(QueryConfig).filter_by(parameter='in_status').first().value.split(',')
        print(countries, with_annotation, not_in_status, in_status)
        return render_template('annotate.html', record = get_record(countries, with_annotation, not_in_status, in_status), most_possible_birds = most_possible_birds, other_possible_birds=other_possible_birds)

    elif request.method == "POST":
        try:
            content_type = request.headers['Content-Type']
            if content_type == 'application/json':
                data = request.get_json()
                recordId = data.pop('recordId')
                for key in data.keys():
                    labels = data[key]
                    birds = [bird for bird in labels if bird in most_possible_birds or bird in other_possible_birds]
                    flags = [flag for flag in labels if flag in flags_list]
                    new_annotation = Annotation(start_time=key.split('-')[0], end_time=key.split('-')[1], label=birds, recording_id=recordId, user_id=current_user.id, status=flags)
                    db_session.add(new_annotation)
            db_session.commit()
            print("Annotation added successfully")
            print(data)
            return "/annotate"
        except Exception as e:
            print(e)
            db_session.rollback()
            flash('Error: ' + str(e))
            return redirect(url_for('route_blueprint.annotate'))
