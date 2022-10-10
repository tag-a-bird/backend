from flask import Flask
from dotenv import load_dotenv
from os import getenv
from flask_restful import Api, Resource
from sqlalchemy import create_engine
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import json
from .models import Base, User, Annotation

load_dotenv()

app = Flask(__name__)

app.config.from_prefixed_env()

db = create_engine(app.config["DATABASE_URI"])

Base.metadata.create_all(db)

api = Api(app)

auth = HTTPBasicAuth()

users = {
    str(getenv("USERNAME")): generate_password_hash(str(getenv("PASSWORD")))
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

class Annotations(Resource):
    @auth.login_required
    def get(self):
        return json.dumps({'Hello': 'World'})

api.add_resource(Annotations, "/api/annotation")

if __name__ == '__main__':
    app.run()