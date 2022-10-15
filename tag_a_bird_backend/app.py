from crypt import methods
from flask import Flask, request, g
from dotenv import load_dotenv
from os import error, getenv
from flask_restful import Api, Resource
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import json
from .models import Base, User, Annotation
import datetime
import uuid


load_dotenv()

app = Flask(__name__)

app.config.from_prefixed_env()

engine = create_engine(app.config["DATABASE_URI"])

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
# Session = sessionmaker(db)  
# session = Session()
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

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username = username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True

class Annotations(Resource):
    @auth.login_required
    def get(self):
        return json.dumps({'Hello': 'World'})

api.add_resource(Annotations, "/api/annotation")

@app.route('/api/signup', methods=['POST'])
def signup():
    db_session.rollback()
    user = User(
            id  = uuid.uuid4(),
            username = request.json.get('username'),
            email = request.json.get('email'),
            created_on = datetime.datetime.now()
            )
    user.set_password(request.json.get('password'))
    db_session.add(user)
    db_session.commit()
    return user.username + " created!" 

if __name__ == '__main__':
    app.run()