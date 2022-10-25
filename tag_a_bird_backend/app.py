from crypt import methods
from flask import Flask, request, jsonify, render_template, flash, url_for, redirect, Blueprint
from flask_restful import Api, Resource
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import datetime
import uuid
import json
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from .helpers import populate_db_from_coreo
from .models import User, Annotation, Base
from . import create_app, auth

route_blueprint = Blueprint('route_blueprint', __name__)

app = create_app()

login_manager = LoginManager(app)

api = Api(app)

engine = create_engine(app.config["DATABASE_URI"])

db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine)
    )

Base.query = db_session.query_property()

Base.metadata.create_all(engine)

@route_blueprint.route('/api/admin', methods=['GET'])
@auth.login_required
def about():
    return 'hello admin'

@login_manager.user_loader
def load_user(user_id):
    return db_session.query(User).get(user_id)

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username = username).first()
    if not user or not user.verify_password(password):
        return False
    return user

class Annotations(Resource):
    @auth.login_required
    def get(self):
        return json.dumps({'Hello': 'World'})

api.add_resource(Annotations, "/api/annotation")

@app.route('/api/signup', methods=['GET', 'POST'])
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
            flash("User successfully registered. You are already logged in. You would be redirected to annotation page if it would be there") # redirect(url_for('login'))
            return render_template('base.html') #redirect(url_for('annotate'))
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
        
@app.route('/api/signin', methods = ["POST", "GET"])
def login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            user = User.query.filter_by(email=email).first()
            if not user or not user.verify_password(password):
                return jsonify({"msg": "Bad username or password"}), 401
            
            login_user(user)
            return "you would be redirected to the annotation page if it was there" #redirect(url_for('annotate_page'))
        except Exception as e:
            print(e)

            return "Error: " + str(e), 500
    elif request.method == 'GET':
        return render_template('auth/login.html')

@app.route('/api/signout', methods=['GET'])
def signout():
    # remove users token from database
    logout_user()
    return redirect(url_for('base.html'))

@app.route('/admin/populate_db', methods = ["GET", "POST"])
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

if __name__ == '__main__':
    app.run()
