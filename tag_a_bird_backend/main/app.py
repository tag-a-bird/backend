import datetime
from os import getenv
import uuid

from utils import models
from utils import db
from . import create_app, config

app = create_app()

if not db.db_session.query(models.User.email == getenv('ADMIN_CREDENTIALS_EMAIL')).first():
    user = models.User(
            id  = uuid.uuid4(),
            username = "admin",
            email= getenv('ADMIN_CREDENTIALS_EMAIL'),
            created_on = datetime.datetime.now()
    )
    user.set_password(getenv('ADMIN_CREDENTIALS_PW'))
    user.roles.append(models.Role(name='Admin'))
    db.db_session.add(user)
    db.db_session.commit()

if __name__ == '__main__':
    app.run()
