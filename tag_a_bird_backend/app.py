import datetime
from os import getenv
import uuid
from . import create_app, config
from .models import User, Role
from .db import db_session
from functools import wraps
from flask import session, jsonify

def access_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            if session.get("role") == 'Admin' and role == 'Admin':
                print("access: Admin")
            else:
                return jsonify({"msg": "Only the admin can access this page"}), 401
            return fn(*args, **kwargs)
        return decorated_function
    return wrapper
    
app = create_app(config.DevConfig)

if not User.query.filter(User.email == getenv('ADMIN_CREDENTIALS_EMAIL')).first():
    user = User(
            id  = uuid.uuid4(),
            username = "admin",
            email= getenv('ADMIN_CREDENTIALS_EMAIL'),
            created_on = datetime.datetime.now()
    )
    user.set_password(getenv('ADMIN_CREDENTIALS_PW'))
    user.roles.append(Role(name='Admin'))
    db_session.add(user)
    db_session.commit()

if __name__ == '__main__':
    app.run()
