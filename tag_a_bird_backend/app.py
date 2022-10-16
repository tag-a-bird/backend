from crypt import methods
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
import datetime
import uuid
from dotenv import load_dotenv
import json

from .models import Base, User, Annotation

app = Flask(__name__)

load_dotenv()

app.config.from_prefixed_env()

jwt = JWTManager(app)

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

def dict_helper(objlist):
    dict = [item.obj_to_dict() for item in objlist]
    return dict

@app.route('/api/users', methods = ["GET"])
def get_users():
    users_info = db_session.query(User).all()
    users_list_dict = dict_helper(users_info)
    return users_list_dict

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/api/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity = username)
    return jsonify(access_token = access_token)

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as = current_user), 200

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username = username).first()
    if not user:
        user = User.query.filter_by(username = username).first()
        if not user or not user.verify_password(password):
            return False
    return user

class Annotations(Resource):
    @auth.login_required
    def get(self):
        return json.dumps({'Hello': 'World'})

api.add_resource(Annotations, "/api/annotation")

@app.route('/api/signup', methods=['POST'])
def signup():
    db_session.rollback()
    try:
        user = User(
                id  = uuid.uuid4(),
                username = request.get_json(force = True)['username'],
                email = request.get_json(force = True)['email'],
                created_on = datetime.datetime.now()
                )
        user.set_password(request.json.get('password'))
        db_session.add(user)
        db_session.commit()
        print("User added")

        return user.username + " created!", 201
    except Exception as e:
        print(e)

        return "Error: " + str(e), 500

if __name__ == '__main__':
    app.run()