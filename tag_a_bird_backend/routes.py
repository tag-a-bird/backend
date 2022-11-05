from flask import request, jsonify, render_template, flash, url_for, redirect, Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from .helpers import populate_db_from_coreo
import datetime
import uuid
from .models import User, QueryConfig
from . import auth, login_manager
from .db import db_session

@login_manager.user_loader
def load_user(user_id):
    return db_session.query(User).get(user_id)

route_blueprint = Blueprint('route_blueprint', __name__,        
    template_folder='templates',
    static_folder='static')

@route_blueprint.route('/api/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
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
            # flash("User successfully registered. You are already logged in. You would be redirected to annotation page if it would be there") # redirect(url_for('login'))
            return render_template('auth/login.html') #redirect(url_for('annotate'))
        except Exception as e:
            db_session.rollback()
            flash('Error: ' + str(e))
            return render_template('base.html')
            # return "Error: " + str(e), 500 
    elif request.method == 'GET':
        if current_user.is_authenticated:
            flash('You are already logged in. You would be redirected to annotation page if it would be there ')
            return render_template('base.html')  #redirect(url_for('annotate'))
        return render_template('auth/signup.html')

@route_blueprint.route('/api/signin', methods = ["POST", "GET"])
def login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            user = User.query.filter_by(email=email).first()
            if not user or not user.verify_password(password):
                return jsonify({"msg": "Bad username or password"}), 401
            
            login_user(user)
            flash("you would be redirected to the annotation page if it was there") #redirect(url_for('annotate_page'))
            return render_template('base.html')
        except Exception as e:
            print(e)

            return "Error: " + str(e), 500
    elif request.method == 'GET':
        if current_user.is_authenticated:
            flash('You are already logged in. You would be redirected to annotation page if it would be there ')
            return render_template('base.html')  #redirect(url_for('annotate'))
        return render_template('auth/login.html')

@route_blueprint.route('/api/signout')
def signout():
    # remove users token from database
    logout_user()
    return redirect(url_for('route_blueprint.login'))

@route_blueprint.route('/admin/populate_db', methods = ["GET", "POST"])
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

@route_blueprint.route('/admin', methods=['GET', 'POST'])
@auth.login_required
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