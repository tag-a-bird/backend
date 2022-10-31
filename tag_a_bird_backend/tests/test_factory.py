from tag_a_bird_backend import config, create_app


def test_config():
    assert create_app().testing 
    assert create_app(config.DevConfig).testing


def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'
