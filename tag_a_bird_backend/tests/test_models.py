'''
classes and methods in models.py are: 
UserRoles, 
User, User.set_password(self, password), User.verify_password(self, password)
Role, 
QueryConfig,
Annotation,
Record, Record.from_json(json, id)
'''
from tag_a_bird_backend.models import QueryConfig, User, Record, Annotation

def test_user_methods(test_user):
    assert test_user.verify_password('testpassword')
    assert test_user.email == 'test@email.com'

def test_query_config(test_query_config):
    test_session = test_query_config
    assert test_session.query(QueryConfig).filter_by(parameter='country').first().value == "Hungary"
    assert test_session.query(QueryConfig).filter_by(parameter='with_annotation').first().value == "False"
    assert test_session.query(QueryConfig).filter_by(parameter='in_status').first().value == ""
    assert test_session.query(QueryConfig).filter_by(parameter='not_in_status').first().value == ""

def test_new_annotation(test_annotation):
    test_session = test_annotation
    assert test_session.query(User).filter_by(username='fakeuser').first().username == "fakeuser"
    # assert test_session.query(Record).first().id == 9811488
    assert test_session.query(Annotation).first().recording_id == 9811488
