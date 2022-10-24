import base64
from tag_a_bird_backend.app import app

def test_admin_unauth():
    web = app.test_client()

    rv = web.get('/api/admin')
    assert rv.status == '401 UNAUTHORIZED'
    assert rv.data == b'Unauthorized Access'
    assert 'WWW-Authenticate' in rv.headers
    assert rv.headers['WWW-Authenticate'] == 'Basic realm="Authentication Required"'

def test_admin_auth():
    web = app.test_client()

    credentials = base64.b64encode(b'kinga:test').decode('utf-8')
    rv = web.get('/api/admin', headers={
            'Authorization': 'Basic ' + credentials
    })

    assert rv.status == '200 OK'
    assert rv.data == b'hello admin'