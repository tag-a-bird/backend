from crypt import methods
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from os import error, getenv
from flask_restful import Api, Resource
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import json
from .models import Base, User, Annotation
import datetime
import uuid


load_dotenv()

app = Flask(__name__)

app.config.from_prefixed_env()

db = create_engine(app.config["DATABASE_URI"])

Session = sessionmaker(db)  
session = Session()

Base.metadata.create_all(db)

api = Api(app)

auth = HTTPBasicAuth()

def dict_helper(objlist):
    dict = [item.obj_to_dict() for item in objlist]
    return dict

@app.route('/api/users', methods = ["GET"])
def get_users():
    users_info = session.query(User).all()
    users_list_dict = dict_helper(users_info)
    return users_list_dict

users = {
    str(getenv("USERNAME")): generate_password_hash(str(getenv("PASSWORD")))
}

# users = get_users()

@auth.verify_password
def verify_password(username, password):
    # users_info = session.query(User).all()
    # users = dict_helper(users_info)
    # if username in users:
    if username in users and check_password_hash(users.get(username), password):
        return username


class Annotations(Resource):
    @auth.login_required
    def get(self):
        return json.dumps({'Hello': 'World'})

api.add_resource(Annotations, "/api/annotation")

@app.route('/api/signup', methods=['POST'])
def signup():
    session.rollback()
    user = User(
            id  = uuid.uuid4(),
            username = request.json.get('username'),
            email = request.json.get('email'),
            created_on = datetime.datetime.now()
            )
    user.set_password(request.json.get('password'))
    session.add(user)
    session.commit()
    return user.username + " created!" 

# @app.route('/login', methods=["POST"])
# def login():
#     res = request.get_json()
#     email_entered = res['email']
#     password_entered = res['password']
#     user = User.query.filter_by(email=email_entered).first()
#     return user

if __name__ == '__main__':
    app.run()