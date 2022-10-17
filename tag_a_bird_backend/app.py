from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_httpauth import HTTPBasicAuth
import datetime
import uuid
from dotenv import load_dotenv
import json
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt

from .models import Base, TokenBlocklist, User, Annotation

app = Flask(__name__)

load_dotenv()

app.config.from_prefixed_env()

ACCESS_EXPIRES = datetime.timedelta(hours=2)

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES

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

class Test(Resource):
    @jwt_required
    def get(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        return json.dumps({ "username": user.username }), 200

api.add_resource(Annotations, "/api/annotation")
api.add_resource(Test, "/api/test")

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

# Create a route to authenticate your users and return JWT Token. The
# create_access_token() function is used to actually generate the JWT.
@app.route('/api/signin', methods = ["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return jsonify({"msg": "Bad username or password"}), 401
    
    # create a new token with the user id inside
    access_token = create_access_token(identity=user.id)
    return jsonify({ "token": access_token, "user_id": user.id })

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db_session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None

# Endpoint for revoking the current users access token. Saved the unique
# identifier (jti) for the JWT into our database.
@app.route('/api/signout', methods=["DELETE"])
@jwt_required()
def modify_token():
    id  = uuid.uuid4()
    jti = get_jwt()["jti"]
    now = datetime.datetime.now()
    db_session.add(TokenBlocklist(id=id, jti=jti, created_at=now))
    db_session.commit()
    return jsonify(msg="JWT revoked")

# example proteceted endpoint
@app.route('/api/protected', methods=["GET"])
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