import datetime
from os import getenv
import uuid
from .models import User, Role
from .db import db_session
from . import create_app, config
from secure import Secure

secure_headers = Secure()
    
app = create_app(config.DevConfig)

@app.after_request
def set_secure_headers(response):
    secure_headers.framework.flask(response)
    return response

if not db_session.query(User.email == getenv('ADMIN_CREDENTIALS_EMAIL')).first():
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
