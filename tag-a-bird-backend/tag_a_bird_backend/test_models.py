from .models import User

def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email and password are defined correctly
    """
    user = User(email = 'patkennedy79@gmail.com', password = 'FlaskIsAwesome')
    assert user.email == 'patkennedy79@gmail.com'
    assert user.password == 'FlaskIsAwesome'
