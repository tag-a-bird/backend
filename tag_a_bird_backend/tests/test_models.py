from tag_a_bird_backend.models import QueryConfig

def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email and verify_password
    """
    assert new_user.verify_password('testpassword')
    assert new_user.email == 'test@email.com'

def test_query_config(test_client, test_data):
    test_session = test_data
    assert test_session.query(QueryConfig).filter_by(parameter='country').first().value == "Hungary"
    assert test_session.query(QueryConfig).filter_by(parameter='with_annotation').first().value == "False"
    assert test_session.query(QueryConfig).filter_by(parameter='in_status').first().value == ""
    assert test_session.query(QueryConfig).filter_by(parameter='not_in_status').first().value == ""

# def test_new_annotation(new_annotation):
#     assert new_annotation.id == 12345