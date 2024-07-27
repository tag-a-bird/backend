from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for, session
from flask_login import login_user, logout_user, current_user
import uuid, datetime
from ...models import User, Role
from ...db import db_session
from ... import login_manager, limiter
from os import getenv

auth_bp = Blueprint('auth', __name__, template_folder='templates', static_folder='static')

@auth_bp.route('/api/register', methods=['GET'])
def register_get():
    if current_user.is_authenticated:
        return render_template('about.html')
    return render_template('auth/register.html')

@auth_bp.route('/api/register', methods=['POST'])
def register_post():
    if len(request.form['password']) > 7:
        if db_session.query(User).filter(User.email == request.form['email']).first() is None:
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
                return render_template('about.html')
            except Exception as e:
                db_session.rollback()
                flash('Error: ' + str(e))
                return render_template('auth/register.html')
        else:
            flash('Error: User already exists')
            return render_template('auth/register.html')
    else:
        flash("The password must be at least 8 characters long!")
        return render_template('auth/register.html')

@auth_bp.route('/api/login', methods=['GET'])
def login_get():
    if current_user.is_authenticated:
        return render_template('about.html')
    return render_template('auth/login.html')

@auth_bp.route('/api/login', methods=['POST'])
@limiter.limit("5 per hour", deduct_when=lambda response: response.status_code != 200)
def login_post():
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
        return render_template('about.html')
    except Exception as e:
        print(e)
        return jsonify({"msg": "Bad email or password"}), 401

@auth_bp.route('/api/logout')
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('auth.login'))

@login_manager.user_loader
def load_user(user_id):
    return db_session.query(User).get(user_id)