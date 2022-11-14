def test_about_route(client):
    assert client.get('/about').status_code == 200

def test_signup_route(client):
    assert client.get('/api/signup').status_code == 200
    # assert client.post('/api/signup').status_code == 200

def test_signin_route(client):
    assert client.get('/api/signin').status_code == 200
    # assert client.post('/api/signin').status_code == 200 

def test_signout_route(client):
    assert client.get('/api/signin').status_code == 200

def test_admin_route(client):
    assert client.get('/admin').status_code == 200

def test_populate_db_route(client):
    assert client.get('/admin/populate_db').status_code == 200

def test_annotate_route(client):
    pass
    # assert client.get('/annotate').status_code == 200