import datetime
import uuid
from .models import User

def test_signup():
    user = User(
        id  = uuid.uuid4(),
        email = 'test@test.com', 
        created_on = datetime.datetime.now()
        )
    user.set_password('FlaskIsAwesome')
    assert user.email == 'test@test.com'
    assert user.verify_password('FlaskIsAwesome')
