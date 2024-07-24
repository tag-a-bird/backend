import datetime
from os import getenv
import uuid
from tag_a_bird_backend.models import User, Role
from tag_a_bird_backend.db import db_session
from tag_a_bird_backend import create_app, config

app = create_app()

@app.before_first_request
def setup_admin_user():
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