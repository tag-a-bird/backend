import datetime
from os import getenv
import uuid
from .models import User, Role
from .db import db_session
from . import create_app

app = create_app()

# Check if the Admin role exists
admin_role = db_session.query(Role).filter_by(name='Admin').first()
if not admin_role:
    admin_role = Role(name='Admin')
    db_session.add(admin_role)
    db_session.commit()

# Check if the admin user exists
if not db_session.query(User).filter_by(email=getenv('ADMIN_CREDENTIALS_EMAIL')).first():
    user = User(
        id=uuid.uuid4(),
        username="admin",
        email=getenv('ADMIN_CREDENTIALS_EMAIL'),
        created_on=datetime.datetime.now()
    )
    user.set_password(getenv('ADMIN_CREDENTIALS_PW'))
    user.roles.append(admin_role)
    db_session.add(user)
    db_session.commit()

if __name__ == '__main__':
    app.run()