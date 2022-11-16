import datetime
import uuid
from . import create_app, config
from .models import User, Role
from .db import db_session, engine

    
app = create_app(config.DevConfig)


if not User.query.filter(User.email == 'admin@admin.com').first():
    user = User(
            id  = uuid.uuid4(),
            username = 'admin',
            email='admin@admin.com',
            created_on = datetime.datetime.now()
    )
    user.set_password('password1')
    user.roles.append(Role(name='Admin'))
    db_session.add(user)
    db_session.commit()

if __name__ == '__main__':
    app.run()
