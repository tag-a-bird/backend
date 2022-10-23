from flask import Flask, request, jsonify, render_template, flash, url_for, redirect
from flask_restful import Api, Resource
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_httpauth import HTTPBasicAuth
import datetime
import uuid
from dotenv import load_dotenv
import json
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_toastr import Toastr
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from .models import Base, User, Annotation

app = Flask(__name__)

load_dotenv()

app.config.from_prefixed_env()

login_manager = LoginManager(app)

engine = create_engine(app.config["DATABASE_URI"])

db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine)
    )

Base.query = db_session.query_property()

Base.metadata.create_all(engine)

api = Api(app)

auth = HTTPBasicAuth()

toastr = Toastr(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



def dict_helper(objlist):
    dict = [item.obj_to_dict() for item in objlist]
    return dict

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username = username).first()
    if not user or not user.verify_password(password):
        return False
    return user

class Annotations(Resource):
    @auth.login_required
    # @jwt_required()
    def get(self):
        return json.dumps({'Hello': 'World'})

class Test(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        return json.dumps({ "username": user.username }), 200

api.add_resource(Annotations, "/api/annotation")
api.add_resource(Test, "/api/test")

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

            return "Error: " + str(e), 500
    elif request.method == 'GET':
        if current_user.is_authenticated:
            flash('You are already logged in. You would be redirected to annotation page if it would be there ')
            return render_template('base.html')  #redirect(url_for('annotate'))
        return render_template('auth/signup.html')
        

# Create a route to authenticate your users and return JWT Token. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/api/signin", methods = ["POST", "GET"])
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


# example proteceted endpoint
@app.route("/api/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    return jsonify({"id": user.id, "username": user.username }), 200

@app.route('/api/users', methods = ["GET"])
@jwt_required()
def get_users():
    users_info = db_session.query(User).all()
    users_list_dict = dict_helper(users_info)
    return users_list_dict


if __name__ == '__main__':
    app.run()