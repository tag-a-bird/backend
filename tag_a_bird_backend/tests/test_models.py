def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email and verify_password
    """
    assert new_user.verify_password('testpassword')
    assert new_user.email == 'test@email.com'

