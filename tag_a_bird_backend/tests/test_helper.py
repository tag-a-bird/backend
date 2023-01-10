from tag_a_bird_backend.utils.helpers import populate_db_from_coreo
from tag_a_bird_backend.utils.models import Record

def test_populate_db(setup_test_database, app):
    temp_session = setup_test_database
    with app.test_request_context("/admin/populate_db", method="POST", data={"country": "Japan"}):
        populate_db_from_coreo(db_session=temp_session, country='Japan')
        assert temp_session.query(Record).first().country == "Japan"
        temp_session.query(Record).delete()
        temp_session.commit()

    # TODO: add more tests for eg. case when there already are some recordings!