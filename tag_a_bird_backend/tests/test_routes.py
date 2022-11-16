def test_about_route(client):
    assert client.get('/about').status_code == 200

def test_register_route(client):
    assert client.get('/api/register').status_code == 200
    # assert client.post('/api/register').status_code == 200

def test_login_route(client):
    assert client.get('/api/login').status_code == 200
    # assert client.post('/api/login').status_code == 200 

def test_logout_route(client):
    assert client.get('/api/login').status_code == 200

# def test_admin_route(client):
#     assert client.get('/admin').status_code == 200

# def test_populate_db_route(client):
#     assert client.get('/admin/populate_db').status_code == 200

def test_annotate_route(client):
    pass
    # assert client.get('/annotate').status_code == 200