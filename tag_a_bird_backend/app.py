from crypt import methods
from flask_restful import Resource
import json
from .models import User, Annotation, Base
from . import create_app, auth, api, config
from .db import db_session
    
app = create_app(config.DevConfig)

Base.query = db_session.query_property()

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username = username).first()
    if not user or not user.verify_password(password):
        return False
    return user

if __name__ == '__main__':
    app.run()
