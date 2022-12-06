'''
routes and http methods are: 
/about - GET
/api/register - GET, POST
/api/login - GET, POST
/api/logout - GET
/admin - GET, POST
/admin/populate_db - GET, POST
/annotate - GET, POST
'''

def test_about_route(test_client):
    assert test_client.get('/about').status_code == 200

def test_register_route(test_client):
    assert test_client.get('/api/register').status_code == 200
    response = test_client.post('/api/register', follow_redirects=True,  data = {
        "username": "tagger",
        "email": "tagabird.FS2022@gmail.com" ,
        "password": "secretsecret",
        })
    assert response.request.path == "/about"
    assert response.status_code == 200

def test_login_route(test_client):
    assert test_client.get('/api/login').status_code == 200
    
def test_logout_route(test_client):
    response = test_client.get('/api/logout', follow_redirects=True)
    assert len(response.history) == 1
    assert response.request.path == "/api/login"
    assert response.status_code == 200

def test_admin_route(test_client, test_query_config):
    assert test_client.get('/admin').status_code == 401
    with test_client.session_transaction() as session:
        session['role'] = "Admin"
    assert test_client.get('/admin').status_code == 200

def test_populate_db_route(test_client):
    assert test_client.get('/admin/populate_db').status_code == 401
    with test_client.session_transaction() as session:
        session['role'] = "Admin"
    assert test_client.get('/admin/populate_db').status_code == 200

def test_annotate_route(test_client, test_query_config):
    assert test_client.get('/annotate').status_code == 200